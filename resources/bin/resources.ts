#!/usr/bin/env node
import "source-map-support/register";
import * as cdk from "aws-cdk-lib";
import { JinstagramStack } from "../lib/resources-stack";

const app = new cdk.App();
new JinstagramStack(app, "JintagramStack", {
    env: { account: process.env.CDK_DEFULAT_ACCOUNT, region: "ap-northeast-2" },
});
