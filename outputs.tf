output "request_bucket_name" {
  value = aws_s3_bucket.request_bucket.bucket
}

output "response_bucket_name" {
  value = aws_s3_bucket.response_bucket.bucket
}

output "lambda_function_name" {
  value = aws_lambda_function.translation_lambda.function_name
}