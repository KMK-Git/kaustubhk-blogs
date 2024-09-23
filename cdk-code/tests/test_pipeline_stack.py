"""
Test CDK Pipelines Stack.
"""

# pylint: disable=line-too-long,too-many-lines
import aws_cdk as cdk
from aws_cdk import assertions
from pipeline_stack.pipeline import PipelineStack
from pipeline_stages.static_website_deploy_stage import StaticWebsiteDeployStage


def test_pipeline_stack() -> None:
    """
    Test CDK Pipelines Stack.
    """
    app = cdk.App()
    stack = PipelineStack(
        app,
        "PipelineStack",
        static_website_deploy_stage=StaticWebsiteDeployStage(
            app,
            "StaticWebsiteDeployStage",
            hostedzone_domain_name="kaustubhk.com",
            website_subdomain="blogs",
            alternative_subdomains=[],
            env=cdk.Environment(account="123456789012", region="ap-south-1"),
        ),
        env=cdk.Environment(account="123456789012", region="ap-south-1"),
    )
    template = assertions.Template.from_stack(stack)
    template.has_resource_properties(
        "AWS::S3::Bucket",
        {
            "BucketEncryption": {
                "ServerSideEncryptionConfiguration": [
                    {"ServerSideEncryptionByDefault": {"SSEAlgorithm": "aws:kms"}}
                ]
            },
            "PublicAccessBlockConfiguration": {
                "BlockPublicAcls": True,
                "BlockPublicPolicy": True,
                "IgnorePublicAcls": True,
                "RestrictPublicBuckets": True,
            },
        },
    )
    template.has_resource_properties(
        "AWS::S3::BucketPolicy",
        {
            "Bucket": {"Ref": "PipelineArtifactsBucketAEA9A052"},
            "PolicyDocument": {
                "Statement": [
                    {
                        "Action": "s3:*",
                        "Condition": {"Bool": {"aws:SecureTransport": "false"}},
                        "Effect": "Deny",
                        "Principal": {"AWS": "*"},
                        "Resource": [
                            {"Fn::GetAtt": ["PipelineArtifactsBucketAEA9A052", "Arn"]},
                            {
                                "Fn::Join": [
                                    "",
                                    [
                                        {
                                            "Fn::GetAtt": [
                                                "PipelineArtifactsBucketAEA9A052",
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
                        "Action": ["s3:GetObject*", "s3:GetBucket*", "s3:List*"],
                        "Effect": "Allow",
                        "Principal": {
                            "AWS": {
                                "Fn::Join": [
                                    "",
                                    [
                                        "arn:",
                                        {"Ref": "AWS::Partition"},
                                        ":iam::123456789012:role/cdk-hnb659fds-deploy-role-123456789012-ap-south-1",
                                    ],
                                ]
                            }
                        },
                        "Resource": [
                            {"Fn::GetAtt": ["PipelineArtifactsBucketAEA9A052", "Arn"]},
                            {
                                "Fn::Join": [
                                    "",
                                    [
                                        {
                                            "Fn::GetAtt": [
                                                "PipelineArtifactsBucketAEA9A052",
                                                "Arn",
                                            ]
                                        },
                                        "/*",
                                    ],
                                ]
                            },
                        ],
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
                        "Principal": {"Service": "codepipeline.amazonaws.com"},
                    }
                ],
                "Version": "2012-10-17",
            }
        },
    )
    template.has_resource_properties(
        "AWS::IAM::Policy",
        {
            "PolicyDocument": {
                "Statement": [
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
                            {"Fn::GetAtt": ["PipelineArtifactsBucketAEA9A052", "Arn"]},
                            {
                                "Fn::Join": [
                                    "",
                                    [
                                        {
                                            "Fn::GetAtt": [
                                                "PipelineArtifactsBucketAEA9A052",
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
                        "Action": "sts:AssumeRole",
                        "Effect": "Allow",
                        "Resource": {
                            "Fn::GetAtt": [
                                "PipelineSourceKMKGitkaustubhkblogsCodePipelineActionRole46D89A7A",
                                "Arn",
                            ]
                        },
                    },
                    {
                        "Action": "sts:AssumeRole",
                        "Effect": "Allow",
                        "Resource": {
                            "Fn::GetAtt": ["PipelineCodeBuildActionRole226DB0CB", "Arn"]
                        },
                    },
                    {
                        "Action": "sts:AssumeRole",
                        "Effect": "Allow",
                        "Resource": {
                            "Fn::GetAtt": [
                                "PipelineStaticWebsiteDeployStageCheckPermissionsCheckCodePipelineActionRole1B886EC9",
                                "Arn",
                            ]
                        },
                    },
                    {
                        "Action": "sts:AssumeRole",
                        "Effect": "Allow",
                        "Resource": {
                            "Fn::GetAtt": [
                                "PipelineStaticWebsiteDeployStageCheckPermissionsConfirmCodePipelineActionRoleD51F04A1",
                                "Arn",
                            ]
                        },
                    },
                    {
                        "Action": "sts:AssumeRole",
                        "Effect": "Allow",
                        "Resource": {
                            "Fn::Join": [
                                "",
                                [
                                    "arn:",
                                    {"Ref": "AWS::Partition"},
                                    ":iam::123456789012:role/cdk-hnb659fds-deploy-role-123456789012-ap-south-1",
                                ],
                            ]
                        },
                    },
                ],
                "Version": "2012-10-17",
            },
            "PolicyName": "PipelineRoleDefaultPolicy7BDC1ABB",
            "Roles": [{"Ref": "PipelineRoleB27FAA37"}],
        },
    )
    template.has_resource_properties(
        "AWS::CodePipeline::Pipeline",
        {
            "ArtifactStore": {
                "Location": {"Ref": "PipelineArtifactsBucketAEA9A052"},
                "Type": "S3",
            },
            "PipelineType": "V1",
            "RestartExecutionOnUpdate": True,
            "RoleArn": {"Fn::GetAtt": ["PipelineRoleB27FAA37", "Arn"]},
            "Stages": [
                {
                    "Actions": [
                        {
                            "ActionTypeId": {
                                "Category": "Source",
                                "Owner": "AWS",
                                "Provider": "CodeStarSourceConnection",
                                "Version": "1",
                            },
                            "Configuration": {
                                "ConnectionArn": {
                                    "Ref": "SsmParameterValuecodestarconnectionarnC96584B6F00A464EAD1953AFF4B05118Parameter"
                                },
                                "FullRepositoryId": "KMK-Git/kaustubhk-blogs",
                                "BranchName": "main",
                            },
                            "Name": "KMK-Git_kaustubhk-blogs",
                            "OutputArtifacts": [
                                {"Name": "KMK_Git_kaustubhk_blogs_Source"}
                            ],
                            "RoleArn": {
                                "Fn::GetAtt": [
                                    "PipelineSourceKMKGitkaustubhkblogsCodePipelineActionRole46D89A7A",
                                    "Arn",
                                ]
                            },
                            "RunOrder": 1,
                        }
                    ],
                    "Name": "Source",
                },
                {
                    "Actions": [
                        {
                            "ActionTypeId": {
                                "Category": "Build",
                                "Owner": "AWS",
                                "Provider": "CodeBuild",
                                "Version": "1",
                            },
                            "Configuration": {
                                "ProjectName": {
                                    "Ref": "PipelineBuildSynthCdkBuildProject6BEFA8E6"
                                },
                                "EnvironmentVariables": '[{"name":"_PROJECT_CONFIG_HASH","type":"PLAINTEXT","value":"22fc5eaa13808ea6f8415167c37918d08190889a013cd637ffe326ff6adb68a1"}]',
                            },
                            "InputArtifacts": [
                                {"Name": "KMK_Git_kaustubhk_blogs_Source"}
                            ],
                            "Name": "Synth",
                            "OutputArtifacts": [{"Name": "Synth_Output"}],
                            "RoleArn": {
                                "Fn::GetAtt": [
                                    "PipelineCodeBuildActionRole226DB0CB",
                                    "Arn",
                                ]
                            },
                            "RunOrder": 1,
                        }
                    ],
                    "Name": "Build",
                },
                {
                    "Actions": [
                        {
                            "ActionTypeId": {
                                "Category": "Build",
                                "Owner": "AWS",
                                "Provider": "CodeBuild",
                                "Version": "1",
                            },
                            "Configuration": {
                                "ProjectName": {
                                    "Ref": "PipelineUpdatePipelineSelfMutationDAA41400"
                                },
                                "EnvironmentVariables": '[{"name":"_PROJECT_CONFIG_HASH","type":"PLAINTEXT","value":"167eef1378d6e6ad8c4c8da3461f900d6e066cd0916052ee812a8d94b87ad38c"}]',
                            },
                            "InputArtifacts": [{"Name": "Synth_Output"}],
                            "Name": "SelfMutate",
                            "RoleArn": {
                                "Fn::GetAtt": [
                                    "PipelineCodeBuildActionRole226DB0CB",
                                    "Arn",
                                ]
                            },
                            "RunOrder": 1,
                        }
                    ],
                    "Name": "UpdatePipeline",
                },
                {
                    "Actions": [
                        {
                            "ActionTypeId": {
                                "Category": "Build",
                                "Owner": "AWS",
                                "Provider": "CodeBuild",
                                "Version": "1",
                            },
                            "Configuration": {
                                "ProjectName": {
                                    "Ref": "PipelineAssetsFileAsset185A67CB4"
                                }
                            },
                            "InputArtifacts": [{"Name": "Synth_Output"}],
                            "Name": "FileAsset1",
                            "RoleArn": {
                                "Fn::GetAtt": [
                                    "PipelineCodeBuildActionRole226DB0CB",
                                    "Arn",
                                ]
                            },
                            "RunOrder": 1,
                        },
                        {
                            "ActionTypeId": {
                                "Category": "Build",
                                "Owner": "AWS",
                                "Provider": "CodeBuild",
                                "Version": "1",
                            },
                            "Configuration": {
                                "ProjectName": {
                                    "Ref": "PipelineAssetsFileAsset24D2D639B"
                                }
                            },
                            "InputArtifacts": [{"Name": "Synth_Output"}],
                            "Name": "FileAsset2",
                            "RoleArn": {
                                "Fn::GetAtt": [
                                    "PipelineCodeBuildActionRole226DB0CB",
                                    "Arn",
                                ]
                            },
                            "RunOrder": 1,
                        },
                        {
                            "ActionTypeId": {
                                "Category": "Build",
                                "Owner": "AWS",
                                "Provider": "CodeBuild",
                                "Version": "1",
                            },
                            "Configuration": {
                                "ProjectName": {
                                    "Ref": "PipelineAssetsFileAsset3FE71B523"
                                }
                            },
                            "InputArtifacts": [{"Name": "Synth_Output"}],
                            "Name": "FileAsset3",
                            "RoleArn": {
                                "Fn::GetAtt": [
                                    "PipelineCodeBuildActionRole226DB0CB",
                                    "Arn",
                                ]
                            },
                            "RunOrder": 1,
                        },
                        {
                            "ActionTypeId": {
                                "Category": "Build",
                                "Owner": "AWS",
                                "Provider": "CodeBuild",
                                "Version": "1",
                            },
                            "Configuration": {
                                "ProjectName": {
                                    "Ref": "PipelineAssetsFileAsset474303B7D"
                                }
                            },
                            "InputArtifacts": [{"Name": "Synth_Output"}],
                            "Name": "FileAsset4",
                            "RoleArn": {
                                "Fn::GetAtt": [
                                    "PipelineCodeBuildActionRole226DB0CB",
                                    "Arn",
                                ]
                            },
                            "RunOrder": 1,
                        },
                    ],
                    "Name": "Assets",
                },
                {
                    "Actions": [
                        {
                            "ActionTypeId": {
                                "Category": "Build",
                                "Owner": "AWS",
                                "Provider": "CodeBuild",
                                "Version": "1",
                            },
                            "Configuration": {
                                "ProjectName": {
                                    "Ref": "PipelinePipelinesSecurityCheckCDKSecurityCheck1D09275A"
                                },
                                "EnvironmentVariables": '[{"name":"STAGE_PATH","type":"PLAINTEXT","value":"StaticWebsiteDeployStage"},{"name":"STAGE_NAME","type":"PLAINTEXT","value":"StaticWebsiteDeployStage"},{"name":"ACTION_NAME","type":"PLAINTEXT","value":"CheckPermissions.Confirm"}]',
                            },
                            "InputArtifacts": [{"Name": "Synth_Output"}],
                            "Name": "CheckPermissions.Check",
                            "Namespace": "c86867a2804b4097e40a75abadbbd14c6423e67f24",
                            "RoleArn": {
                                "Fn::GetAtt": [
                                    "PipelineStaticWebsiteDeployStageCheckPermissionsCheckCodePipelineActionRole1B886EC9",
                                    "Arn",
                                ]
                            },
                            "RunOrder": 1,
                        },
                        {
                            "ActionTypeId": {
                                "Category": "Approval",
                                "Owner": "AWS",
                                "Provider": "Manual",
                                "Version": "1",
                            },
                            "Configuration": {
                                "CustomData": "#{c86867a2804b4097e40a75abadbbd14c6423e67f24.MESSAGE}",
                                "ExternalEntityLink": "#{c86867a2804b4097e40a75abadbbd14c6423e67f24.LINK}",
                            },
                            "Name": "CheckPermissions.Confirm",
                            "RoleArn": {
                                "Fn::GetAtt": [
                                    "PipelineStaticWebsiteDeployStageCheckPermissionsConfirmCodePipelineActionRoleD51F04A1",
                                    "Arn",
                                ]
                            },
                            "RunOrder": 2,
                        },
                        {
                            "ActionTypeId": {
                                "Category": "Deploy",
                                "Owner": "AWS",
                                "Provider": "CloudFormation",
                                "Version": "1",
                            },
                            "Configuration": {
                                "StackName": "StaticWebsiteDeployStage-StaticWebsiteStack",
                                "Capabilities": "CAPABILITY_NAMED_IAM,CAPABILITY_AUTO_EXPAND",
                                "RoleArn": {
                                    "Fn::Join": [
                                        "",
                                        [
                                            "arn:",
                                            {"Ref": "AWS::Partition"},
                                            ":iam::123456789012:role/cdk-hnb659fds-cfn-exec-role-123456789012-ap-south-1",
                                        ],
                                    ]
                                },
                                "ActionMode": "CHANGE_SET_REPLACE",
                                "ChangeSetName": "PipelineChange",
                                "TemplatePath": "Synth_Output::assembly-StaticWebsiteDeployStage/StaticWebsiteDeployStageStaticWebsiteStack733D8CA8.template.json",
                            },
                            "InputArtifacts": [{"Name": "Synth_Output"}],
                            "Name": "StaticWebsiteStack.Prepare",
                            "RoleArn": {
                                "Fn::Join": [
                                    "",
                                    [
                                        "arn:",
                                        {"Ref": "AWS::Partition"},
                                        ":iam::123456789012:role/cdk-hnb659fds-deploy-role-123456789012-ap-south-1",
                                    ],
                                ]
                            },
                            "RunOrder": 3,
                        },
                        {
                            "ActionTypeId": {
                                "Category": "Deploy",
                                "Owner": "AWS",
                                "Provider": "CloudFormation",
                                "Version": "1",
                            },
                            "Configuration": {
                                "StackName": "StaticWebsiteDeployStage-StaticWebsiteStack",
                                "ActionMode": "CHANGE_SET_EXECUTE",
                                "ChangeSetName": "PipelineChange",
                            },
                            "Name": "StaticWebsiteStack.Deploy",
                            "RoleArn": {
                                "Fn::Join": [
                                    "",
                                    [
                                        "arn:",
                                        {"Ref": "AWS::Partition"},
                                        ":iam::123456789012:role/cdk-hnb659fds-deploy-role-123456789012-ap-south-1",
                                    ],
                                ]
                            },
                            "RunOrder": 4,
                        },
                    ],
                    "Name": "StaticWebsiteDeployStage",
                },
            ],
            "Tags": [{"Key": "SECURITY_CHECK", "Value": "ALLOW_APPROVE"}],
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
                        "Principal": {
                            "AWS": {
                                "Fn::Join": [
                                    "",
                                    [
                                        "arn:",
                                        {"Ref": "AWS::Partition"},
                                        ":iam::123456789012:root",
                                    ],
                                ]
                            }
                        },
                    }
                ],
                "Version": "2012-10-17",
            }
        },
    )
    template.has_resource_properties(
        "AWS::IAM::Policy",
        {
            "PolicyDocument": {
                "Statement": [
                    {
                        "Action": "codestar-connections:UseConnection",
                        "Effect": "Allow",
                        "Resource": {
                            "Ref": "SsmParameterValuecodestarconnectionarnC96584B6F00A464EAD1953AFF4B05118Parameter"
                        },
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
                            {"Fn::GetAtt": ["PipelineArtifactsBucketAEA9A052", "Arn"]},
                            {
                                "Fn::Join": [
                                    "",
                                    [
                                        {
                                            "Fn::GetAtt": [
                                                "PipelineArtifactsBucketAEA9A052",
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
                        "Action": ["s3:PutObjectAcl", "s3:PutObjectVersionAcl"],
                        "Effect": "Allow",
                        "Resource": {
                            "Fn::Join": [
                                "",
                                [
                                    {
                                        "Fn::GetAtt": [
                                            "PipelineArtifactsBucketAEA9A052",
                                            "Arn",
                                        ]
                                    },
                                    "/*",
                                ],
                            ]
                        },
                    },
                ],
                "Version": "2012-10-17",
            },
            "PolicyName": "PipelineSourceKMKGitkaustubhkblogsCodePipelineActionRoleDefaultPolicy82688263",
            "Roles": [
                {
                    "Ref": "PipelineSourceKMKGitkaustubhkblogsCodePipelineActionRole46D89A7A"
                }
            ],
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
                        "Principal": {"Service": "codebuild.amazonaws.com"},
                    }
                ],
                "Version": "2012-10-17",
            }
        },
    )
    template.has_resource_properties(
        "AWS::IAM::Policy",
        {
            "PolicyDocument": {
                "Statement": [
                    {
                        "Action": [
                            "logs:CreateLogGroup",
                            "logs:CreateLogStream",
                            "logs:PutLogEvents",
                        ],
                        "Effect": "Allow",
                        "Resource": [
                            {
                                "Fn::Join": [
                                    "",
                                    [
                                        "arn:",
                                        {"Ref": "AWS::Partition"},
                                        ":logs:ap-south-1:123456789012:log-group:/aws/codebuild/",
                                        {
                                            "Ref": "PipelineBuildSynthCdkBuildProject6BEFA8E6"
                                        },
                                    ],
                                ]
                            },
                            {
                                "Fn::Join": [
                                    "",
                                    [
                                        "arn:",
                                        {"Ref": "AWS::Partition"},
                                        ":logs:ap-south-1:123456789012:log-group:/aws/codebuild/",
                                        {
                                            "Ref": "PipelineBuildSynthCdkBuildProject6BEFA8E6"
                                        },
                                        ":*",
                                    ],
                                ]
                            },
                        ],
                    },
                    {
                        "Action": [
                            "codebuild:CreateReportGroup",
                            "codebuild:CreateReport",
                            "codebuild:UpdateReport",
                            "codebuild:BatchPutTestCases",
                            "codebuild:BatchPutCodeCoverages",
                        ],
                        "Effect": "Allow",
                        "Resource": {
                            "Fn::Join": [
                                "",
                                [
                                    "arn:",
                                    {"Ref": "AWS::Partition"},
                                    ":codebuild:ap-south-1:123456789012:report-group/",
                                    {
                                        "Ref": "PipelineBuildSynthCdkBuildProject6BEFA8E6"
                                    },
                                    "-*",
                                ],
                            ]
                        },
                    },
                    {
                        "Action": "sts:AssumeRole",
                        "Condition": {
                            "StringEquals": {
                                "iam:ResourceTag/aws-cdk:bootstrap-role": "lookup"
                            }
                        },
                        "Effect": "Allow",
                        "Resource": "*",
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
                            {"Fn::GetAtt": ["PipelineArtifactsBucketAEA9A052", "Arn"]},
                            {
                                "Fn::Join": [
                                    "",
                                    [
                                        {
                                            "Fn::GetAtt": [
                                                "PipelineArtifactsBucketAEA9A052",
                                                "Arn",
                                            ]
                                        },
                                        "/*",
                                    ],
                                ]
                            },
                        ],
                    },
                ],
                "Version": "2012-10-17",
            },
            "PolicyName": "PipelineBuildSynthCdkBuildProjectRoleDefaultPolicyFB6C941C",
            "Roles": [{"Ref": "PipelineBuildSynthCdkBuildProjectRole231EEA2A"}],
        },
    )
    template.has_resource_properties(
        "AWS::CodeBuild::Project",
        {
            "Artifacts": {"Type": "CODEPIPELINE"},
            "Cache": {"Type": "NO_CACHE"},
            "Description": "Pipeline step PipelineStack/Pipeline/Build/Synth",
            "EncryptionKey": "alias/aws/s3",
            "Environment": {
                "ComputeType": "BUILD_GENERAL1_SMALL",
                "Image": "aws/codebuild/standard:7.0",
                "ImagePullCredentialsType": "CODEBUILD",
                "PrivilegedMode": False,
                "Type": "LINUX_CONTAINER",
            },
            "ServiceRole": {
                "Fn::GetAtt": ["PipelineBuildSynthCdkBuildProjectRole231EEA2A", "Arn"]
            },
            "Source": {
                "BuildSpec": '{\n  "version": "0.2",\n  "phases": {\n    "install": {\n      "commands": [\n        "cd site-code",\n        "npm ci",\n        "cd ../cdk-code",\n        "pip install -r requirements.txt -r requirements-dev.txt",\n        "npm install -g aws-cdk"\n      ]\n    },\n    "build": {\n      "commands": [\n        "cd ../site-code",\n        "npm run lint",\n        "npm run test",\n        "npm run build",\n        "cd ../cdk-code",\n        "black .",\n        "pylint application_stacks pipeline_stages pipeline_stack tests app.py",\n        "pytest --cov=.",\n        "cdk synth"\n      ]\n    }\n  },\n  "artifacts": {\n    "base-directory": "cdk-code/cdk.out",\n    "files": "**/*"\n  }\n}',
                "Type": "CODEPIPELINE",
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
                        "Principal": {
                            "AWS": {
                                "Fn::Join": [
                                    "",
                                    [
                                        "arn:",
                                        {"Ref": "AWS::Partition"},
                                        ":iam::123456789012:root",
                                    ],
                                ]
                            }
                        },
                    }
                ],
                "Version": "2012-10-17",
            }
        },
    )
    template.has_resource_properties(
        "AWS::IAM::Policy",
        {
            "PolicyDocument": {
                "Statement": [
                    {
                        "Action": [
                            "codebuild:BatchGetBuilds",
                            "codebuild:StartBuild",
                            "codebuild:StopBuild",
                        ],
                        "Effect": "Allow",
                        "Resource": {
                            "Fn::GetAtt": [
                                "PipelinePipelinesSecurityCheckCDKSecurityCheck1D09275A",
                                "Arn",
                            ]
                        },
                    }
                ],
                "Version": "2012-10-17",
            },
            "PolicyName": "PipelineStaticWebsiteDeployStageCheckPermissionsCheckCodePipelineActionRoleDefaultPolicy541F68EC",
            "Roles": [
                {
                    "Ref": "PipelineStaticWebsiteDeployStageCheckPermissionsCheckCodePipelineActionRole1B886EC9"
                }
            ],
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
                        "Principal": {
                            "AWS": {
                                "Fn::Join": [
                                    "",
                                    [
                                        "arn:",
                                        {"Ref": "AWS::Partition"},
                                        ":iam::123456789012:root",
                                    ],
                                ]
                            }
                        },
                    }
                ],
                "Version": "2012-10-17",
            }
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
                        "Principal": {
                            "AWS": {"Fn::GetAtt": ["PipelineRoleB27FAA37", "Arn"]}
                        },
                    }
                ],
                "Version": "2012-10-17",
            }
        },
    )
    template.has_resource_properties(
        "AWS::IAM::Policy",
        {
            "PolicyDocument": {
                "Statement": [
                    {
                        "Action": [
                            "codebuild:BatchGetBuilds",
                            "codebuild:StartBuild",
                            "codebuild:StopBuild",
                        ],
                        "Effect": "Allow",
                        "Resource": {
                            "Fn::GetAtt": [
                                "PipelineBuildSynthCdkBuildProject6BEFA8E6",
                                "Arn",
                            ]
                        },
                    },
                    {
                        "Action": [
                            "codebuild:BatchGetBuilds",
                            "codebuild:StartBuild",
                            "codebuild:StopBuild",
                        ],
                        "Effect": "Allow",
                        "Resource": {
                            "Fn::GetAtt": [
                                "PipelineUpdatePipelineSelfMutationDAA41400",
                                "Arn",
                            ]
                        },
                    },
                    {
                        "Action": [
                            "codebuild:BatchGetBuilds",
                            "codebuild:StartBuild",
                            "codebuild:StopBuild",
                        ],
                        "Effect": "Allow",
                        "Resource": {
                            "Fn::GetAtt": ["PipelineAssetsFileAsset185A67CB4", "Arn"]
                        },
                    },
                    {
                        "Action": [
                            "codebuild:BatchGetBuilds",
                            "codebuild:StartBuild",
                            "codebuild:StopBuild",
                        ],
                        "Effect": "Allow",
                        "Resource": {
                            "Fn::GetAtt": ["PipelineAssetsFileAsset24D2D639B", "Arn"]
                        },
                    },
                    {
                        "Action": [
                            "codebuild:BatchGetBuilds",
                            "codebuild:StartBuild",
                            "codebuild:StopBuild",
                        ],
                        "Effect": "Allow",
                        "Resource": {
                            "Fn::GetAtt": ["PipelineAssetsFileAsset3FE71B523", "Arn"]
                        },
                    },
                    {
                        "Action": [
                            "codebuild:BatchGetBuilds",
                            "codebuild:StartBuild",
                            "codebuild:StopBuild",
                        ],
                        "Effect": "Allow",
                        "Resource": {
                            "Fn::GetAtt": ["PipelineAssetsFileAsset474303B7D", "Arn"]
                        },
                    },
                ],
                "Version": "2012-10-17",
            },
            "PolicyName": "PipelineCodeBuildActionRoleDefaultPolicy1D62A6FE",
            "Roles": [{"Ref": "PipelineCodeBuildActionRole226DB0CB"}],
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
                        "Principal": {"Service": "codebuild.amazonaws.com"},
                    }
                ],
                "Version": "2012-10-17",
            }
        },
    )
    template.has_resource_properties(
        "AWS::IAM::Policy",
        {
            "PolicyDocument": {
                "Statement": [
                    {
                        "Action": [
                            "logs:CreateLogGroup",
                            "logs:CreateLogStream",
                            "logs:PutLogEvents",
                        ],
                        "Effect": "Allow",
                        "Resource": [
                            {
                                "Fn::Join": [
                                    "",
                                    [
                                        "arn:",
                                        {"Ref": "AWS::Partition"},
                                        ":logs:ap-south-1:123456789012:log-group:/aws/codebuild/",
                                        {
                                            "Ref": "PipelineUpdatePipelineSelfMutationDAA41400"
                                        },
                                    ],
                                ]
                            },
                            {
                                "Fn::Join": [
                                    "",
                                    [
                                        "arn:",
                                        {"Ref": "AWS::Partition"},
                                        ":logs:ap-south-1:123456789012:log-group:/aws/codebuild/",
                                        {
                                            "Ref": "PipelineUpdatePipelineSelfMutationDAA41400"
                                        },
                                        ":*",
                                    ],
                                ]
                            },
                        ],
                    },
                    {
                        "Action": [
                            "codebuild:CreateReportGroup",
                            "codebuild:CreateReport",
                            "codebuild:UpdateReport",
                            "codebuild:BatchPutTestCases",
                            "codebuild:BatchPutCodeCoverages",
                        ],
                        "Effect": "Allow",
                        "Resource": {
                            "Fn::Join": [
                                "",
                                [
                                    "arn:",
                                    {"Ref": "AWS::Partition"},
                                    ":codebuild:ap-south-1:123456789012:report-group/",
                                    {
                                        "Ref": "PipelineUpdatePipelineSelfMutationDAA41400"
                                    },
                                    "-*",
                                ],
                            ]
                        },
                    },
                    {
                        "Action": "sts:AssumeRole",
                        "Condition": {
                            "ForAnyValue:StringEquals": {
                                "iam:ResourceTag/aws-cdk:bootstrap-role": [
                                    "image-publishing",
                                    "file-publishing",
                                    "deploy",
                                ]
                            }
                        },
                        "Effect": "Allow",
                        "Resource": "arn:*:iam::123456789012:role/*",
                    },
                    {
                        "Action": "cloudformation:DescribeStacks",
                        "Effect": "Allow",
                        "Resource": "*",
                    },
                    {"Action": "s3:ListBucket", "Effect": "Allow", "Resource": "*"},
                    {
                        "Action": ["s3:GetObject*", "s3:GetBucket*", "s3:List*"],
                        "Effect": "Allow",
                        "Resource": [
                            {"Fn::GetAtt": ["PipelineArtifactsBucketAEA9A052", "Arn"]},
                            {
                                "Fn::Join": [
                                    "",
                                    [
                                        {
                                            "Fn::GetAtt": [
                                                "PipelineArtifactsBucketAEA9A052",
                                                "Arn",
                                            ]
                                        },
                                        "/*",
                                    ],
                                ]
                            },
                        ],
                    },
                ],
                "Version": "2012-10-17",
            },
            "PolicyName": "PipelineUpdatePipelineSelfMutationRoleDefaultPolicyA225DA4E",
            "Roles": [{"Ref": "PipelineUpdatePipelineSelfMutationRole57E559E8"}],
        },
    )
    template.has_resource_properties(
        "AWS::CodeBuild::Project",
        {
            "Artifacts": {"Type": "CODEPIPELINE"},
            "Cache": {"Type": "NO_CACHE"},
            "Description": "Pipeline step PipelineStack/Pipeline/UpdatePipeline/SelfMutate",
            "EncryptionKey": "alias/aws/s3",
            "Environment": {
                "ComputeType": "BUILD_GENERAL1_SMALL",
                "Image": "aws/codebuild/standard:7.0",
                "ImagePullCredentialsType": "CODEBUILD",
                "PrivilegedMode": False,
                "Type": "LINUX_CONTAINER",
            },
            "ServiceRole": {
                "Fn::GetAtt": ["PipelineUpdatePipelineSelfMutationRole57E559E8", "Arn"]
            },
            "Source": {
                "BuildSpec": '{\n  "version": "0.2",\n  "phases": {\n    "install": {\n      "commands": [\n        "npm install -g aws-cdk@2"\n      ]\n    },\n    "build": {\n      "commands": [\n        "cdk -a . deploy PipelineStack --require-approval=never --verbose"\n      ]\n    }\n  }\n}',
                "Type": "CODEPIPELINE",
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
                        "Principal": {"Service": "codebuild.amazonaws.com"},
                    },
                    {
                        "Action": "sts:AssumeRole",
                        "Effect": "Allow",
                        "Principal": {
                            "AWS": {
                                "Fn::Join": [
                                    "",
                                    [
                                        "arn:",
                                        {"Ref": "AWS::Partition"},
                                        ":iam::123456789012:root",
                                    ],
                                ]
                            }
                        },
                    },
                ],
                "Version": "2012-10-17",
            }
        },
    )
    template.has_resource_properties(
        "AWS::IAM::Policy",
        {
            "PolicyDocument": {
                "Statement": [
                    {
                        "Action": [
                            "logs:CreateLogGroup",
                            "logs:CreateLogStream",
                            "logs:PutLogEvents",
                        ],
                        "Effect": "Allow",
                        "Resource": {
                            "Fn::Join": [
                                "",
                                [
                                    "arn:",
                                    {"Ref": "AWS::Partition"},
                                    ":logs:ap-south-1:123456789012:log-group:/aws/codebuild/*",
                                ],
                            ]
                        },
                    },
                    {
                        "Action": [
                            "codebuild:CreateReportGroup",
                            "codebuild:CreateReport",
                            "codebuild:UpdateReport",
                            "codebuild:BatchPutTestCases",
                            "codebuild:BatchPutCodeCoverages",
                        ],
                        "Effect": "Allow",
                        "Resource": {
                            "Fn::Join": [
                                "",
                                [
                                    "arn:",
                                    {"Ref": "AWS::Partition"},
                                    ":codebuild:ap-south-1:123456789012:report-group/*",
                                ],
                            ]
                        },
                    },
                    {
                        "Action": [
                            "codebuild:BatchGetBuilds",
                            "codebuild:StartBuild",
                            "codebuild:StopBuild",
                        ],
                        "Effect": "Allow",
                        "Resource": "*",
                    },
                    {
                        "Action": "sts:AssumeRole",
                        "Effect": "Allow",
                        "Resource": {
                            "Fn::Sub": "arn:${AWS::Partition}:iam::123456789012:role/cdk-hnb659fds-file-publishing-role-123456789012-ap-south-1"
                        },
                    },
                    {
                        "Action": ["s3:GetObject*", "s3:GetBucket*", "s3:List*"],
                        "Effect": "Allow",
                        "Resource": [
                            {"Fn::GetAtt": ["PipelineArtifactsBucketAEA9A052", "Arn"]},
                            {
                                "Fn::Join": [
                                    "",
                                    [
                                        {
                                            "Fn::GetAtt": [
                                                "PipelineArtifactsBucketAEA9A052",
                                                "Arn",
                                            ]
                                        },
                                        "/*",
                                    ],
                                ]
                            },
                        ],
                    },
                ],
                "Version": "2012-10-17",
            },
            "PolicyName": "PipelineAssetsFileRoleDefaultPolicy14DB8755",
            "Roles": [{"Ref": "PipelineAssetsFileRole59943A77"}],
        },
    )
    template.has_resource_properties(
        "AWS::CodeBuild::Project",
        {
            "Artifacts": {"Type": "CODEPIPELINE"},
            "Cache": {"Type": "NO_CACHE"},
            "Description": "Pipeline step PipelineStack/Pipeline/Assets/FileAsset1",
            "EncryptionKey": "alias/aws/s3",
            "Environment": {
                "ComputeType": "BUILD_GENERAL1_SMALL",
                "Image": "aws/codebuild/standard:7.0",
                "ImagePullCredentialsType": "CODEBUILD",
                "PrivilegedMode": False,
                "Type": "LINUX_CONTAINER",
            },
            "ServiceRole": {"Fn::GetAtt": ["PipelineAssetsFileRole59943A77", "Arn"]},
            "Source": {
                "BuildSpec": '{\n  "version": "0.2",\n  "phases": {\n    "install": {\n      "commands": [\n        "npm install -g cdk-assets@2"\n      ]\n    },\n    "build": {\n      "commands": [\n        "cdk-assets --path \\"assembly-StaticWebsiteDeployStage/StaticWebsiteDeployStageStaticWebsiteStack733D8CA8.assets.json\\" --verbose publish \\"b073cebcf4d61fb152a30f5a5e57a94df7f980a549fdf1a79a0b18c5750522d8:123456789012-ap-south-1\\""\n      ]\n    }\n  }\n}',
                "Type": "CODEPIPELINE",
            },
        },
    )
    template.has_resource_properties(
        "AWS::CodeBuild::Project",
        {
            "Artifacts": {"Type": "CODEPIPELINE"},
            "Cache": {"Type": "NO_CACHE"},
            "Description": "Pipeline step PipelineStack/Pipeline/Assets/FileAsset2",
            "EncryptionKey": "alias/aws/s3",
            "Environment": {
                "ComputeType": "BUILD_GENERAL1_SMALL",
                "Image": "aws/codebuild/standard:7.0",
                "ImagePullCredentialsType": "CODEBUILD",
                "PrivilegedMode": False,
                "Type": "LINUX_CONTAINER",
            },
            "ServiceRole": {"Fn::GetAtt": ["PipelineAssetsFileRole59943A77", "Arn"]},
            "Source": {
                "BuildSpec": '{\n  "version": "0.2",\n  "phases": {\n    "install": {\n      "commands": [\n        "npm install -g cdk-assets@2"\n      ]\n    },\n    "build": {\n      "commands": [\n        "cdk-assets --path \\"assembly-StaticWebsiteDeployStage/StaticWebsiteDeployStageStaticWebsiteStack733D8CA8.assets.json\\" --verbose publish \\"60e7451b2fd9c1305b623d09d2e42ce9024e794b76786e135dd5744dac6d8832:123456789012-ap-south-1\\""\n      ]\n    }\n  }\n}',
                "Type": "CODEPIPELINE",
            },
        },
    )
    template.has_resource_properties(
        "AWS::CodeBuild::Project",
        {
            "Artifacts": {"Type": "CODEPIPELINE"},
            "Cache": {"Type": "NO_CACHE"},
            "Description": "Pipeline step PipelineStack/Pipeline/Assets/FileAsset3",
            "EncryptionKey": "alias/aws/s3",
            "Environment": {
                "ComputeType": "BUILD_GENERAL1_SMALL",
                "Image": "aws/codebuild/standard:7.0",
                "ImagePullCredentialsType": "CODEBUILD",
                "PrivilegedMode": False,
                "Type": "LINUX_CONTAINER",
            },
            "ServiceRole": {"Fn::GetAtt": ["PipelineAssetsFileRole59943A77", "Arn"]},
            "Source": {
                "BuildSpec": '{\n  "version": "0.2",\n  "phases": {\n    "install": {\n      "commands": [\n        "npm install -g cdk-assets@2"\n      ]\n    },\n    "build": {\n      "commands": [\n        "cdk-assets --path \\"assembly-StaticWebsiteDeployStage/StaticWebsiteDeployStageStaticWebsiteStack733D8CA8.assets.json\\" --verbose publish \\"2d56e153cac88d3e0c2f842e8e6f6783b8725bf91f95e0673b4725448a56e96d:123456789012-ap-south-1\\""\n      ]\n    }\n  }\n}',
                "Type": "CODEPIPELINE",
            },
        },
    )
    template.has_resource_properties(
        "AWS::CodeBuild::Project",
        {
            "Artifacts": {"Type": "CODEPIPELINE"},
            "Cache": {"Type": "NO_CACHE"},
            "Description": "Pipeline step PipelineStack/Pipeline/Assets/FileAsset4",
            "EncryptionKey": "alias/aws/s3",
            "Environment": {
                "ComputeType": "BUILD_GENERAL1_SMALL",
                "Image": "aws/codebuild/standard:7.0",
                "ImagePullCredentialsType": "CODEBUILD",
                "PrivilegedMode": False,
                "Type": "LINUX_CONTAINER",
            },
            "ServiceRole": {"Fn::GetAtt": ["PipelineAssetsFileRole59943A77", "Arn"]},
            "Source": {
                "Type": "CODEPIPELINE",
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
                            "codepipeline:GetPipelineState",
                            "codepipeline:PutApprovalResult",
                        ],
                        "Condition": {
                            "StringEquals": {
                                "aws:ResourceTag/SECURITY_CHECK": "ALLOW_APPROVE"
                            }
                        },
                        "Effect": "Allow",
                        "Resource": "*",
                    }
                ],
                "Version": "2012-10-17",
            },
            "PolicyName": "PipelinePipelinesSecurityCheckCDKPipelinesAutoApproveServiceRoleDefaultPolicy334C3224",
            "Roles": [
                {
                    "Ref": "PipelinePipelinesSecurityCheckCDKPipelinesAutoApproveServiceRoleC48D6A44"
                }
            ],
        },
    )
    template.has_resource_properties(
        "AWS::Lambda::Function",
        {
            "Code": {
                "S3Bucket": "cdk-hnb659fds-assets-123456789012-ap-south-1",
                "S3Key": "8f5a1090fc6972a51e904601772d6525545251717845601746ed5307556368a8.zip",
            },
            "Handler": "index.handler",
            "Role": {
                "Fn::GetAtt": [
                    "PipelinePipelinesSecurityCheckCDKPipelinesAutoApproveServiceRoleC48D6A44",
                    "Arn",
                ]
            },
            "Runtime": "nodejs18.x",
            "Timeout": 300,
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
                        "Principal": {"Service": "codebuild.amazonaws.com"},
                    }
                ],
                "Version": "2012-10-17",
            }
        },
    )
    template.has_resource_properties(
        "AWS::IAM::Policy",
        {
            "PolicyDocument": {
                "Statement": [
                    {
                        "Action": [
                            "logs:CreateLogGroup",
                            "logs:CreateLogStream",
                            "logs:PutLogEvents",
                        ],
                        "Effect": "Allow",
                        "Resource": [
                            {
                                "Fn::Join": [
                                    "",
                                    [
                                        "arn:",
                                        {"Ref": "AWS::Partition"},
                                        ":logs:ap-south-1:123456789012:log-group:/aws/codebuild/",
                                        {
                                            "Ref": "PipelinePipelinesSecurityCheckCDKSecurityCheck1D09275A"
                                        },
                                    ],
                                ]
                            },
                            {
                                "Fn::Join": [
                                    "",
                                    [
                                        "arn:",
                                        {"Ref": "AWS::Partition"},
                                        ":logs:ap-south-1:123456789012:log-group:/aws/codebuild/",
                                        {
                                            "Ref": "PipelinePipelinesSecurityCheckCDKSecurityCheck1D09275A"
                                        },
                                        ":*",
                                    ],
                                ]
                            },
                        ],
                    },
                    {
                        "Action": [
                            "codebuild:CreateReportGroup",
                            "codebuild:CreateReport",
                            "codebuild:UpdateReport",
                            "codebuild:BatchPutTestCases",
                            "codebuild:BatchPutCodeCoverages",
                        ],
                        "Effect": "Allow",
                        "Resource": {
                            "Fn::Join": [
                                "",
                                [
                                    "arn:",
                                    {"Ref": "AWS::Partition"},
                                    ":codebuild:ap-south-1:123456789012:report-group/",
                                    {
                                        "Ref": "PipelinePipelinesSecurityCheckCDKSecurityCheck1D09275A"
                                    },
                                    "-*",
                                ],
                            ]
                        },
                    },
                    {
                        "Action": "sts:AssumeRole",
                        "Condition": {
                            "ForAnyValue:StringEquals": {
                                "iam:ResourceTag/aws-cdk:bootstrap-role": ["deploy"]
                            }
                        },
                        "Effect": "Allow",
                        "Resource": "*",
                    },
                    {
                        "Action": "lambda:InvokeFunction",
                        "Effect": "Allow",
                        "Resource": [
                            {
                                "Fn::GetAtt": [
                                    "PipelinePipelinesSecurityCheckCDKPipelinesAutoApprove438244C8",
                                    "Arn",
                                ]
                            },
                            {
                                "Fn::Join": [
                                    "",
                                    [
                                        {
                                            "Fn::GetAtt": [
                                                "PipelinePipelinesSecurityCheckCDKPipelinesAutoApprove438244C8",
                                                "Arn",
                                            ]
                                        },
                                        ":*",
                                    ],
                                ]
                            },
                        ],
                    },
                    {
                        "Action": ["s3:GetObject*", "s3:GetBucket*", "s3:List*"],
                        "Effect": "Allow",
                        "Resource": [
                            {"Fn::GetAtt": ["PipelineArtifactsBucketAEA9A052", "Arn"]},
                            {
                                "Fn::Join": [
                                    "",
                                    [
                                        {
                                            "Fn::GetAtt": [
                                                "PipelineArtifactsBucketAEA9A052",
                                                "Arn",
                                            ]
                                        },
                                        "/*",
                                    ],
                                ]
                            },
                        ],
                    },
                ],
                "Version": "2012-10-17",
            },
            "PolicyName": "PipelinePipelinesSecurityCheckCDKSecurityCheckRoleDefaultPolicy6675DA4A",
            "Roles": [
                {"Ref": "PipelinePipelinesSecurityCheckCDKSecurityCheckRole62A863BD"}
            ],
        },
    )
    template.has_resource_properties(
        "AWS::CodeBuild::Project",
        {
            "Artifacts": {"Type": "NO_ARTIFACTS"},
            "Cache": {"Type": "NO_CACHE"},
            "EncryptionKey": "alias/aws/s3",
            "Environment": {
                "ComputeType": "BUILD_GENERAL1_SMALL",
                "Image": "aws/codebuild/standard:7.0",
                "ImagePullCredentialsType": "CODEBUILD",
                "PrivilegedMode": False,
                "Type": "LINUX_CONTAINER",
            },
            "ServiceRole": {
                "Fn::GetAtt": [
                    "PipelinePipelinesSecurityCheckCDKSecurityCheckRole62A863BD",
                    "Arn",
                ]
            },
            "Source": {
                "BuildSpec": {
                    "Fn::Join": [
                        "",
                        [
                            '{\n  "version": 0.2,\n  "phases": {\n    "build": {\n      "commands": [\n        "npm install -g aws-cdk",\n        "export PIPELINE_NAME=\\"$(node -pe \'`${process.env.CODEBUILD_INITIATOR}`.split(\\"/\\")[1]\')\\"",\n        "payload=\\"$(node -pe \'JSON.stringify({ \\"PipelineName\\": process.env.PIPELINE_NAME, \\"StageName\\": process.env.STAGE_NAME, \\"ActionName\\": process.env.ACTION_NAME })\' )\\"",\n        "ARN=$CODEBUILD_BUILD_ARN",\n        "REGION=\\"$(node -pe \'`${process.env.ARN}`.split(\\":\\")[3]\')\\"",\n        "ACCOUNT_ID=\\"$(node -pe \'`${process.env.ARN}`.split(\\":\\")[4]\')\\"",\n        "PROJECT_NAME=\\"$(node -pe \'`${process.env.ARN}`.split(\\":\\")[5].split(\\"/\\")[1]\')\\"",\n        "PROJECT_ID=\\"$(node -pe \'`${process.env.ARN}`.split(\\":\\")[6]\')\\"",\n        "export LINK=\\"https://$REGION.console.aws.amazon.com/codesuite/codebuild/$ACCOUNT_ID/projects/$PROJECT_NAME/build/$PROJECT_NAME:$PROJECT_ID/?region=$REGION\\"",\n        "export PIPELINE_LINK=\\"https://$REGION.console.aws.amazon.com/codesuite/codepipeline/pipelines/$PIPELINE_NAME/view?region=$REGION\\"",\n        "if cdk diff -a . --security-only --fail $STAGE_PATH/\\\\*; then aws lambda invoke --function-name ',
                            {
                                "Ref": "PipelinePipelinesSecurityCheckCDKPipelinesAutoApprove438244C8"
                            },
                            ' --invocation-type Event --cli-binary-format raw-in-base64-out --payload \\"$payload\\" lambda.out; export MESSAGE=\\"No security-impacting changes detected.\\"; else [ -z \\"${NOTIFICATION_ARN}\\" ] || aws sns publish --topic-arn $NOTIFICATION_ARN --subject \\"$NOTIFICATION_SUBJECT\\" --message \\"An upcoming change would broaden security changes in $PIPELINE_NAME.\\nReview and approve the changes in CodePipeline to proceed with the deployment.\\n\\nReview the changes in CodeBuild:\\n\\n$LINK\\n\\nApprove the changes in CodePipeline (stage $STAGE_NAME, action $ACTION_NAME):\\n\\n$PIPELINE_LINK\\"; export MESSAGE=\\"Deployment would make security-impacting changes. Click the link below to inspect them, then click Approve if all changes are expected.\\"; fi"\n      ]\n    }\n  },\n  "env": {\n    "exported-variables": [\n      "LINK",\n      "MESSAGE"\n    ]\n  }\n}',
                        ],
                    ]
                },
                "Type": "NO_SOURCE",
            },
        },
    )
