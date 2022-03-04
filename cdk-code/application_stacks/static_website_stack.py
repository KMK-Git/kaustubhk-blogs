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
    aws_iam as iam,
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
        hosted_zone = route53.HostedZone.from_lookup(
            self, "HostedZone", domain_name=hostedzone_domain_name
        )
        website_domain = website_subdomain + "." + hostedzone_domain_name
        cloudfront_oai = cloudfront.OriginAccessIdentity(
            self, "CloudfrontOAI", comment=f"OAI for {website_domain}"
        )
        website_bucket = s3.Bucket(
            self,
            "WebsiteBucket",
            website_index_document="index.html",
            website_error_document="404.html",
            public_read_access=False,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
        )
        website_bucket.add_to_resource_policy(
            iam.PolicyStatement(
                actions=["s3:GetObject"],
                resources=[website_bucket.arn_for_objects("*)")],
                principals=[
                    iam.CanonicalUserPrincipal(
                        cloudfront_oai.cloud_front_origin_access_identity_s3_canonical_user_id
                    )
                ],
            )
        )
        certificate = acm.DnsValidatedCertificate(
            self,
            "SiteCertificate",
            domain_name=website_domain,
            hosted_zone=hosted_zone,
            region="us-east-1",
        )
        viewer_certificate = cloudfront.ViewerCertificate.from_acm_certificate(
            certificate,
            ssl_method=cloudfront.SSLMethod.SNI,
            security_policy=cloudfront.SecurityPolicyProtocol.TLS_V1_2_2021,
            aliases=[website_domain],
        )
        # pylint: disable=too-many-function-args
        distribution = cloudfront.CloudFrontWebDistribution(
            self,
            "WebsiteDistribution",
            viewer_certificate=viewer_certificate,
            origin_configs=[
                cloudfront.SourceConfiguration(
                    s3_origin_source=cloudfront.S3OriginConfig(
                        s3_bucket_source=website_bucket,
                        origin_access_identity=cloudfront_oai,
                    ),
                    behaviors=[
                        cloudfront.Behavior(
                            is_default_behavior=True,
                            compress=True,
                            allowed_methods=cloudfront.CloudFrontAllowedMethods.GET_HEAD_OPTIONS,
                        )
                    ],
                )
            ],
        )
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
