"""
Test Static Website Stack.
"""
# pylint: disable=line-too-long
import aws_cdk as cdk
from aws_cdk import assertions

from application_stacks.static_website_stack import StaticWebsiteStack


def test_static_website_stack() -> None:
    """
    Test Static Website Stack.
    """
    app = cdk.App()
    stack = StaticWebsiteStack(
        app,
        "StaticWebsiteStack",
        hostedzone_domain_name="example.com",
        website_subdomain="subdomain",
        env=cdk.Environment(account="123456789012", region="ap-south-1"),
    )
    template = assertions.Template.from_stack(stack)
    template.has_resource_properties(
        "AWS::CloudFront::CloudFrontOriginAccessIdentity",
        {
            "CloudFrontOriginAccessIdentityConfig": {
                "Comment": "OAI for subdomain.example.com"
            }
        },
    )
    template.has_resource_properties(
        "AWS::S3::Bucket",
        {
            "PublicAccessBlockConfiguration": {
                "BlockPublicAcls": True,
                "BlockPublicPolicy": True,
                "IgnorePublicAcls": True,
                "RestrictPublicBuckets": True,
            },
            "Tags": [{"Key": "aws-cdk:cr-owned:33647188", "Value": "true"}],
            "WebsiteConfiguration": {
                "ErrorDocument": "404.html",
                "IndexDocument": "index.html",
            },
        },
    )
    template.has_resource_properties(
        "AWS::S3::BucketPolicy",
        {
            "Bucket": {"Ref": "WebsiteBucket75C24D94"},
            "PolicyDocument": {
                "Statement": [
                    {
                        "Action": "s3:GetObject",
                        "Effect": "Allow",
                        "Principal": {
                            "CanonicalUser": {
                                "Fn::GetAtt": [
                                    "CloudfrontOAI6D521D0D",
                                    "S3CanonicalUserId",
                                ]
                            }
                        },
                        "Resource": {
                            "Fn::Join": [
                                "",
                                [
                                    {"Fn::GetAtt": ["WebsiteBucket75C24D94", "Arn"]},
                                    "/*",
                                ],
                            ]
                        },
                    },
                ],
                "Version": "2012-10-17",
            },
        },
    )
    template.has_resource_properties(
        "AWS::IAM::Role",
        {
            "AssumeRolePolicyDocument": {
                "Statement": [
                    {
                        "Action": "sts:AssumeRole",
                        "Effect": "Allow",
                        "Principal": {"Service": "lambda.amazonaws.com"},
                    }
                ],
                "Version": "2012-10-17",
            },
            "ManagedPolicyArns": [
                {
                    "Fn::Join": [
                        "",
                        [
                            "arn:",
                            {"Ref": "AWS::Partition"},
                            ":iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
                        ],
                    ]
                }
            ],
        },
    )
    template.has_resource_properties(
        "AWS::IAM::Policy",
        {
            "PolicyDocument": {
                "Statement": [
                    {
                        "Action": [
                            "acm:RequestCertificate",
                            "acm:DescribeCertificate",
                            "acm:DeleteCertificate",
                            "acm:AddTagsToCertificate",
                        ],
                        "Effect": "Allow",
                        "Resource": "*",
                    },
                    {"Action": "route53:GetChange", "Effect": "Allow", "Resource": "*"},
                    {
                        "Action": "route53:changeResourceRecordSets",
                        "Effect": "Allow",
                        "Resource": {
                            "Fn::Join": [
                                "",
                                [
                                    "arn:",
                                    {"Ref": "AWS::Partition"},
                                    ":route53:::hostedzone/DUMMY",
                                ],
                            ]
                        },
                    },
                ],
                "Version": "2012-10-17",
            },
            "PolicyName": "SiteCertificateCertificateRequestorFunctionServiceRoleDefaultPolicy96ED5C9C",
            "Roles": [
                {
                    "Ref": "SiteCertificateCertificateRequestorFunctionServiceRole645E891D"
                }
            ],
        },
    )
    template.has_resource_properties(
        "AWS::Lambda::Function",
        {
            "Code": {
                "S3Bucket": "cdk-hnb659fds-assets-123456789012-ap-south-1",
            },
            "Role": {
                "Fn::GetAtt": [
                    "SiteCertificateCertificateRequestorFunctionServiceRole645E891D",
                    "Arn",
                ]
            },
            "Handler": "index.certificateRequestHandler",
            "Runtime": "nodejs12.x",
            "Timeout": 900,
        },
    )
    template.has_resource_properties(
        "AWS::CloudFormation::CustomResource",
        {
            "ServiceToken": {
                "Fn::GetAtt": [
                    "SiteCertificateCertificateRequestorFunction7CFA7DEA",
                    "Arn",
                ]
            },
            "DomainName": "subdomain.example.com",
            "HostedZoneId": "DUMMY",
            "Region": "us-east-1",
        },
    )
    template.has_resource_properties(
        "AWS::CloudFront::Distribution",
        {
            "DistributionConfig": {
                "Aliases": ["subdomain.example.com"],
                "DefaultCacheBehavior": {
                    "AllowedMethods": ["GET", "HEAD", "OPTIONS"],
                    "CachedMethods": ["GET", "HEAD"],
                    "Compress": True,
                    "ForwardedValues": {
                        "Cookies": {"Forward": "none"},
                        "QueryString": False,
                    },
                    "TargetOriginId": "origin1",
                    "ViewerProtocolPolicy": "redirect-to-https",
                },
                "DefaultRootObject": "index.html",
                "Enabled": True,
                "HttpVersion": "http2",
                "IPV6Enabled": True,
                "Origins": [
                    {
                        "ConnectionAttempts": 3,
                        "ConnectionTimeout": 10,
                        "DomainName": {
                            "Fn::GetAtt": [
                                "WebsiteBucket75C24D94",
                                "RegionalDomainName",
                            ]
                        },
                        "Id": "origin1",
                        "S3OriginConfig": {
                            "OriginAccessIdentity": {
                                "Fn::Join": [
                                    "",
                                    [
                                        "origin-access-identity/cloudfront/",
                                        {"Ref": "CloudfrontOAI6D521D0D"},
                                    ],
                                ]
                            }
                        },
                    }
                ],
                "PriceClass": "PriceClass_100",
                "ViewerCertificate": {
                    "AcmCertificateArn": {
                        "Fn::GetAtt": [
                            "SiteCertificateCertificateRequestorResource6021082A",
                            "Arn",
                        ]
                    },
                    "MinimumProtocolVersion": "TLSv1.2_2021",
                    "SslSupportMethod": "sni-only",
                },
            }
        },
    )
    template.has_resource_properties(
        "AWS::Route53::RecordSet",
        {
            "Name": "subdomain.example.com.",
            "Type": "A",
            "AliasTarget": {
                "DNSName": {
                    "Fn::GetAtt": [
                        "WebsiteDistributionCFDistribution70408E7F",
                        "DomainName",
                    ]
                },
                "HostedZoneId": {
                    "Fn::FindInMap": [
                        "AWSCloudFrontPartitionHostedZoneIdMap",
                        {"Ref": "AWS::Partition"},
                        "zoneId",
                    ]
                },
            },
            "HostedZoneId": "DUMMY",
        },
    )
    template.has_resource_properties(
        "AWS::Lambda::LayerVersion",
        {
            "Content": {
                "S3Bucket": "cdk-hnb659fds-assets-123456789012-ap-south-1",
            },
            "Description": "/opt/awscli/aws",
        },
    )
    template.has_resource_properties(
        "Custom::CDKBucketDeployment",
        {
            "ServiceToken": {
                "Fn::GetAtt": [
                    "CustomCDKBucketDeployment8693BB64968944B69AAFB0CC9EB8756C81C01536",
                    "Arn",
                ]
            },
            "SourceBucketNames": ["cdk-hnb659fds-assets-123456789012-ap-south-1"],
            "DestinationBucketName": {"Ref": "WebsiteBucket75C24D94"},
            "Prune": True,
            "DistributionId": {"Ref": "WebsiteDistributionCFDistribution70408E7F"},
            "DistributionPaths": ["/*"],
        },
    )
    template.has_resource_properties(
        "AWS::IAM::Role",
        {
            "AssumeRolePolicyDocument": {
                "Statement": [
                    {
                        "Action": "sts:AssumeRole",
                        "Effect": "Allow",
                        "Principal": {"Service": "lambda.amazonaws.com"},
                    }
                ],
                "Version": "2012-10-17",
            },
            "ManagedPolicyArns": [
                {
                    "Fn::Join": [
                        "",
                        [
                            "arn:",
                            {"Ref": "AWS::Partition"},
                            ":iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
                        ],
                    ]
                }
            ],
        },
    )
    template.has_resource_properties(
        "AWS::IAM::Policy",
        {
            "PolicyDocument": {
                "Statement": [
                    {
                        "Action": ["s3:GetObject*", "s3:GetBucket*", "s3:List*"],
                        "Effect": "Allow",
                        "Resource": [
                            {
                                "Fn::Join": [
                                    "",
                                    [
                                        "arn:",
                                        {"Ref": "AWS::Partition"},
                                        ":s3:::cdk-hnb659fds-assets-123456789012-ap-south-1",
                                    ],
                                ]
                            },
                            {
                                "Fn::Join": [
                                    "",
                                    [
                                        "arn:",
                                        {"Ref": "AWS::Partition"},
                                        ":s3:::cdk-hnb659fds-assets-123456789012-ap-south-1/*",
                                    ],
                                ]
                            },
                        ],
                    },
                    {
                        "Action": [
                            "s3:GetObject*",
                            "s3:GetBucket*",
                            "s3:List*",
                            "s3:DeleteObject*",
                            "s3:PutObject",
                            "s3:PutObjectLegalHold",
                            "s3:PutObjectRetention",
                            "s3:PutObjectTagging",
                            "s3:PutObjectVersionTagging",
                            "s3:Abort*",
                        ],
                        "Effect": "Allow",
                        "Resource": [
                            {"Fn::GetAtt": ["WebsiteBucket75C24D94", "Arn"]},
                            {
                                "Fn::Join": [
                                    "",
                                    [
                                        {
                                            "Fn::GetAtt": [
                                                "WebsiteBucket75C24D94",
                                                "Arn",
                                            ]
                                        },
                                        "/*",
                                    ],
                                ]
                            },
                        ],
                    },
                    {
                        "Action": [
                            "cloudfront:GetInvalidation",
                            "cloudfront:CreateInvalidation",
                        ],
                        "Effect": "Allow",
                        "Resource": "*",
                    },
                ],
                "Version": "2012-10-17",
            },
            "PolicyName": "CustomCDKBucketDeployment8693BB64968944B69AAFB0CC9EB8756CServiceRoleDefaultPolicy88902FDF",
            "Roles": [
                {
                    "Ref": "CustomCDKBucketDeployment8693BB64968944B69AAFB0CC9EB8756CServiceRole89A01265"
                }
            ],
        },
    )
    template.has_resource_properties(
        "AWS::Lambda::Function",
        {
            "Code": {
                "S3Bucket": "cdk-hnb659fds-assets-123456789012-ap-south-1",
            },
            "Role": {
                "Fn::GetAtt": [
                    "CustomCDKBucketDeployment8693BB64968944B69AAFB0CC9EB8756CServiceRole89A01265",
                    "Arn",
                ]
            },
            "Handler": "index.handler",
            "Layers": [{"Ref": "S3DeploymentAwsCliLayer8AAFE44F"}],
            "Runtime": "python3.7",
            "Timeout": 900,
        },
    )
