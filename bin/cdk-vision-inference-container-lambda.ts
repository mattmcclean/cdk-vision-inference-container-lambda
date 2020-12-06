#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { CdkVisionInferenceContainerLambdaStack } from '../lib/cdk-vision-inference-container-lambda-stack';

const app = new cdk.App();
new CdkVisionInferenceContainerLambdaStack(app, 'CdkVisionInferenceContainerLambdaStack');
