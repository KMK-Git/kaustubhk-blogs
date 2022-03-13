"""
Static Website CDK Stack.
"""
import os
from aws_cdk import (
    CfnOutput,
    Stack,
    aws_route53 as route53,
    aws_s3 as s3,
    aws_certificatemanager as acm,
    aws_route53_targets as targets,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_s3_deployment as s3deploy,
)
from constructs import Construct


class StaticWebsiteStack(Stack):
    """
    Create infrastructure required for a static application in AWS.
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        hostedzone_domain_name: str,
        website_subdomain: str,
        **kwargs,
    ) -> None:
        """
        Create infrastructure required for a static application in AWS.
        :param scope: Scope in which stack is created.
        :param construct_id: ID of stack construct.
        :param hostedzone_domain_name: Domain name of Route 53 hosted zone.
        :param website_subdomain: Subdomain for static website.
        :param kwargs: Extra keyword arguments.
        """
        super().__init__(scope, construct_id, **kwargs)
        # https://github.com/aws-samples/aws-cdk-examples/blob/master/typescript/static-site/static-site.ts
        # Route 53 Hosted Zone lookup
        hosted_zone = route53.HostedZone.from_lookup(
            self, "HostedZone", domain_name=hostedzone_domain_name
        )
        if website_subdomain is None or website_subdomain == "":
            website_domain = hostedzone_domain_name
        else:
            website_domain = website_subdomain + "." + hostedzone_domain_name
        # S3 bucket where we store our website's static content.
        # We don't allow public access.
        website_bucket = s3.Bucket(
            self,
            "WebsiteBucket",
            public_read_access=False,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
        )
        # Create ACM Certificate for CloudFront distribution.
        certificate = acm.DnsValidatedCertificate(
            self,
            "SiteCertificate",
            domain_name=website_domain,
            hosted_zone=hosted_zone,
            region="us-east-1",
        )
        # Rewrite blog/example to blog/example/index.html, required for Gatsby.
        # https://github.com/aws-samples/amazon-cloudfront-functions/tree/main/url-rewrite-single-page-apps
        cloudfront_function = cloudfront.Function(
            self,
            "CloudfrontFunction",
            code=cloudfront.FunctionCode.from_file(
                file_path="application_stacks/cloudfront_function.js"
            ),
        )
        # Create CloudFront distribution.
        # pylint: disable=too-many-function-args
        distribution = cloudfront.Distribution(
            self,
            "WebsiteDistribution",
            certificate=certificate,
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(website_bucket),
                function_associations=[
                    cloudfront.FunctionAssociation(
                        function=cloudfront_function,
                        event_type=cloudfront.FunctionEventType.VIEWER_REQUEST,
                    )
                ],
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            ),
            domain_names=[website_domain],
            minimum_protocol_version=cloudfront.SecurityPolicyProtocol.TLS_V1_2_2021,
        )
        # pylint: enable=too-many-function-args
        route53.ARecord(
            self,
            "DomainRecord",
            zone=hosted_zone,
            record_name=website_domain,
            target=route53.RecordTarget.from_alias(
                targets.CloudFrontTarget(distribution)
            ),
        )
        s3deploy.BucketDeployment(
            self,
            "S3Deployment",
            sources=[s3deploy.Source.asset(os.path.join("..", "site-code", "public"))],
            destination_bucket=website_bucket,
            distribution=distribution,
            distribution_paths=["/*"],
        )
        CfnOutput(self, "WebsiteDomain", value=f"https://{website_domain}")
        CfnOutput(self, "BucketName", value=website_bucket.bucket_name)
        CfnOutput(self, "CertificateArn", value=certificate.certificate_arn)
        CfnOutput(self, "DistributionId", value=distribution.distribution_id)
