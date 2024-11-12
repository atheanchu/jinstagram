import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";
import * as opensearch from "aws-cdk-lib/aws-opensearchservice";
import { Secret } from "aws-cdk-lib/aws-secretsmanager";
import { aws_s3 as s3 } from "aws-cdk-lib";

export class JinstagramStack extends cdk.Stack {
    constructor(scope: Construct, id: string, props?: cdk.StackProps) {
        super(scope, id, props);

        const encryptionAtRestOptionsProperty: opensearch.CfnDomain.EncryptionAtRestOptionsProperty =
            {
                enabled: false,
            };

        // create secrets in AWS secret manager
        const secret = new Secret(this, "JinstagramSecret", {
            generateSecretString: {
                secretStringTemplate: JSON.stringify({ adminUser: "master" }),
                generateStringKey: "adminPassword!",
                excludePunctuation: true,
            },
        });

        // Create S3 bucket for static files
        const bucket = new s3.Bucket(this, "JinstagramS3Bucket");

        const domain = new opensearch.Domain(this, "JinstagramDomain", {
            version: opensearch.EngineVersion.OPENSEARCH_2_15,
            capacity: {
                dataNodes: 3,
                dataNodeInstanceType: "r6g.xlarge.search",
                multiAzWithStandbyEnabled: false,
            },
            ebs: {
                volumeSize: 10,
                volumeType:
                    cdk.aws_ec2.EbsDeviceVolumeType.GENERAL_PURPOSE_SSD_GP3,
            },
            zoneAwareness: {
                enabled: true,
                availabilityZoneCount: 3,
            },
            nodeToNodeEncryption: true,
            enforceHttps: true,
            useUnsignedBasicAuth: true,
            encryptionAtRest: {
                enabled: true,
            },
            fineGrainedAccessControl: {
                masterUserName: secret
                    .secretValueFromJson("adminUser")
                    .unsafeUnwrap(),
                masterUserPassword: secret.secretValue,
            },
        });

        // Print domain endpoint of Amazon OpenSearch Services
        new cdk.CfnOutput(this, "DomainEndpoint", {
            value: domain.domainEndpoint,
        });

        // Print S3 full bucket path
        new cdk.CfnOutput(this, "S3BucketPath", {
            value: bucket.bucketName,
        });
    }
}
