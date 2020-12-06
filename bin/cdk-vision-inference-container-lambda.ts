#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { VisionInferenceStack } from '../lib/vision-container-lambda-stack';

const app = new cdk.App();
new VisionInferenceStack(app, 'MyVisionInferenceStack');
