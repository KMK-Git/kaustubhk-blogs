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
        alternative_subdomains=[],
        env=cdk.Environment(account="123456789012", region="ap-south-1"),
    )
    template = assertions.Template.from_stack(stack)
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
                                    "WebsiteDistributionOrigin1S3Origin432B5882",
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
                    }
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
                "S3Key": "4d3f21fe611d8ebfd4f1f69754b7f986fed4ecf648d4fafe941cd81ede6cf60c.zip",
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
        "AWS::CloudFront::Function",
        {
            "AutoPublish": True,
            "FunctionCode": "// https://github.com/aws-samples/amazon-cloudfront-functions/tree/main/url-rewrite-single-page-apps\nfunction handler(event) {\n    var request = event.request;\n    var uri = request.uri;\n\n    // Check whether the URI is missing a file name.\n    if (uri.endsWith('/')) {\n        request.uri += 'index.html';\n    }\n    // Check whether the URI is missing a file extension.\n    else if (!uri.includes('.')) {\n        request.uri += '/index.html';\n    }\n\n    return request;\n}",
            "FunctionConfig": {
                "Runtime": "cloudfront-js-1.0",
            },
        },
    )
    template.has_resource_properties(
        "AWS::CloudFront::CloudFrontOriginAccessIdentity",
        {"CloudFrontOriginAccessIdentityConfig": {}},
    )
    template.has_resource_properties(
        "AWS::CloudFront::ResponseHeadersPolicy",
        {
            "ResponseHeadersPolicyConfig": {
                "Comment": "Security Headers",
                "Name": "kaustubhkblogs-SecurityHeadersPolicy",
                "SecurityHeadersConfig": {
                    "ContentSecurityPolicy": {
                        "ContentSecurityPolicy": "default-src 'self'; img-src 'self' data: https://*; child-src 'none'; object-src 'none'; script-src 'unsafe-inline' 'self' 'unsafe-eval'; style-src 'unsafe-inline' 'self'; font-src 'self' data:; frame-src youtube.com www.youtube.com;",
                        "Override": True,
                    },
                    "ContentTypeOptions": {"Override": True},
                    "FrameOptions": {"FrameOption": "DENY", "Override": True},
                    "ReferrerPolicy": {
                        "Override": True,
                        "ReferrerPolicy": "no-referrer",
                    },
                    "StrictTransportSecurity": {
                        "AccessControlMaxAgeSec": 63072000,
                        "IncludeSubdomains": True,
                        "Override": True,
                        "Preload": True,
                    },
                    "XSSProtection": {
                        "ModeBlock": True,
                        "Override": True,
                        "Protection": True,
                    },
                },
            }
        },
    )
    template.has_resource_properties(
        "AWS::CloudFront::Distribution",
        {
            "DistributionConfig": {
                "Aliases": ["subdomain.example.com"],
                "CustomErrorResponses": [
                    {
                        "ErrorCode": 403,
                        "ResponseCode": 404,
                        "ResponsePagePath": "/404.html",
                    }
                ],
                "DefaultCacheBehavior": {
                    "CachePolicyId": "658327ea-f89d-4fab-a63d-7e88639e58f6",
                    "Compress": True,
                    "FunctionAssociations": [
                        {
                            "EventType": "viewer-request",
                            "FunctionARN": {
                                "Fn::GetAtt": [
                                    "CloudfrontFunction11FEE36B",
                                    "FunctionARN",
                                ]
                            },
                        }
                    ],
                    "ResponseHeadersPolicyId": {"Ref": "ResponseHeadersPolicy13DBF9E0"},
                    "ViewerProtocolPolicy": "redirect-to-https",
                },
                "Enabled": True,
                "HttpVersion": "http2",
                "IPV6Enabled": True,
                "Origins": [
                    {
                        "DomainName": {
                            "Fn::GetAtt": [
                                "WebsiteBucket75C24D94",
                                "RegionalDomainName",
                            ]
                        },
                        "S3OriginConfig": {
                            "OriginAccessIdentity": {
                                "Fn::Join": [
                                    "",
                                    [
                                        "origin-access-identity/cloudfront/",
                                        {
                                            "Ref": "WebsiteDistributionOrigin1S3Origin432B5882"
                                        },
                                    ],
                                ]
                            }
                        },
                    }
                ],
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
                    "Fn::GetAtt": ["WebsiteDistribution75DCDA0B", "DomainName"]
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
        "AWS::Route53::RecordSet",
        {
            "Name": "subdomain.example.com.",
            "Type": "AAAA",
            "AliasTarget": {
                "DNSName": {
                    "Fn::GetAtt": ["WebsiteDistribution75DCDA0B", "DomainName"]
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
                "S3Key": "391a62714930dde9689f73f04bec0cd78494b9d9b7167446e54c6c939bbbb6b4.zip",
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
            "DistributionId": {"Ref": "WebsiteDistribution75DCDA0B"},
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
                "S3Key": "f98b78092dcdd31f5e6d47489beb5f804d4835ef86a8085d0a2053cb9ae711da.zip",
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
