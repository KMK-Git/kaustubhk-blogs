"""
Static Website CDK Stack.
"""
import os
from typing import List

from aws_cdk import (
    CfnOutput,
    Stack,
    Duration,
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

    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-locals
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        hostedzone_domain_name: str,
        website_subdomain: str,
        alternative_subdomains: List[str],
        **kwargs,
    ) -> None:
        """
        Create infrastructure required for a static application in AWS.
        :param scope: Scope in which stack is created.
        :param construct_id: ID of stack construct.
        :param hostedzone_domain_name: Domain name of Route 53 hosted zone.
        :param website_subdomain: Subdomain for static website.
        :param alternative_subdomains: List of alternative subdomains,
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
        alternative_domains = []
        for alternative_subdomain in alternative_subdomains:
            if alternative_subdomain is None or alternative_subdomain == "":
                alternative_domains.append(hostedzone_domain_name)
            else:
                alternative_domains.append(
                    alternative_subdomain + "." + hostedzone_domain_name
                )
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
            subject_alternative_names=alternative_domains,
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
        # Add Security Response Headers.
        response_header_policy = cloudfront.ResponseHeadersPolicy(
            self,
            "ResponseHeadersPolicy",
            comment="Security Headers",
            response_headers_policy_name="kaustubhkblogs-SecurityHeadersPolicy",
            security_headers_behavior=cloudfront.ResponseSecurityHeadersBehavior(
                content_security_policy=cloudfront.ResponseHeadersContentSecurityPolicy(
                    content_security_policy="default-src 'self'; "
                    "img-src 'self' data: https://*; child-src 'none'; "
                    "object-src 'none'; script-src 'unsafe-inline' 'self' 'unsafe-eval'; "
                    "style-src 'unsafe-inline' 'self'; font-src 'self' data:;",
                    override=True,
                ),
                content_type_options=cloudfront.ResponseHeadersContentTypeOptions(
                    override=True
                ),
                frame_options=cloudfront.ResponseHeadersFrameOptions(
                    frame_option=cloudfront.HeadersFrameOption.DENY, override=True
                ),
                referrer_policy=cloudfront.ResponseHeadersReferrerPolicy(
                    referrer_policy=cloudfront.HeadersReferrerPolicy.NO_REFERRER,
                    override=True,
                ),
                strict_transport_security=cloudfront.ResponseHeadersStrictTransportSecurity(
                    access_control_max_age=Duration.seconds(63072000),
                    include_subdomains=True,
                    override=True,
                    preload=True,
                ),
                xss_protection=cloudfront.ResponseHeadersXSSProtection(
                    protection=True,
                    mode_block=True,
                    override=True,
                ),
            ),
        )
        # Create CloudFront distribution.
        # pylint: disable=too-many-function-args
        distribution = cloudfront.Distribution(
            self,
            "WebsiteDistribution",
            certificate=certificate,
            error_responses=[
                cloudfront.ErrorResponse(
                    http_status=403,
                    response_http_status=404,
                    response_page_path="/404.html",
                )
            ],
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(website_bucket),
                function_associations=[
                    cloudfront.FunctionAssociation(
                        function=cloudfront_function,
                        event_type=cloudfront.FunctionEventType.VIEWER_REQUEST,
                    )
                ],
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                response_headers_policy=response_header_policy,
            ),
            domain_names=[website_domain] + alternative_domains,
            minimum_protocol_version=cloudfront.SecurityPolicyProtocol.TLS_V1_2_2021,
        )
        # pylint: enable=too-many-function-args
        # Create domain records.
        # ipv4 records.
        route53.ARecord(
            self,
            "DomainRecord",
            zone=hosted_zone,
            record_name=website_domain,
            target=route53.RecordTarget.from_alias(
                targets.CloudFrontTarget(distribution)
            ),
        )
        # ipv6 records.
        route53.AaaaRecord(
            self,
            "DomainRecordAAAA",
            zone=hosted_zone,
            record_name=website_domain,
            target=route53.RecordTarget.from_alias(
                targets.CloudFrontTarget(distribution)
            ),
        )
        for index, alternative_domain in enumerate(alternative_domains):
            # ipv4 records.
            route53.ARecord(
                self,
                f"DomainRecord{index}",
                zone=hosted_zone,
                record_name=alternative_domain,
                target=route53.RecordTarget.from_alias(
                    targets.CloudFrontTarget(distribution)
                ),
            )
            # ipv6 records.
            route53.AaaaRecord(
                self,
                f"DomainRecordAAAA{index}",
                zone=hosted_zone,
                record_name=alternative_domain,
                target=route53.RecordTarget.from_alias(
                    targets.CloudFrontTarget(distribution)
                ),
            )
        # Deploy static content to S3 bucket
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
