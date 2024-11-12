#!/usr/bin/env node
import "source-map-support/register";
import * as cdk from "aws-cdk-lib";
import { JinstagramResourcesStack } from "../lib/jinstagram_resources-stack";

const app = new cdk.App();
new JinstagramResourcesStack(app, "JinstagramResourcesStack", {
    env: { account: process.env.CDK_DEFULAT_ACCOUNT, region: "ap-northeast-2" },
});
