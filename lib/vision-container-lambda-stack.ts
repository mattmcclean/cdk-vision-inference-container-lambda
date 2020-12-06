import * as cdk from '@aws-cdk/core';
import * as vision_service from '../lib/vision-inference-service';

export class VisionInferenceStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);
    
    // Create a new inference service
    new vision_service.VisionInferenceService(this, 'InferenceService');
  }
}
