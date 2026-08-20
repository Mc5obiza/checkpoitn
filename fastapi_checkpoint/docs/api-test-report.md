# API Test Results

## GET /health

Status code: 200

Result: Passed

Notes: API returned status ok.

## POST /chat valid message

Status code: 200

Result: Passed

Notes: Response included `answer`, `model`, and `tokens_used`.

## POST /quiz valid request

Status code: 200

Result: Passed

Notes: Response returned a quiz containing 5 questions, each with options and the correct answer.

## POST /summarise valid request

Status code: 200

Result: Passed

Notes: Response returned a summary with 5 bullet points, along with the model and `tokens_used`.

## POST /chat missing message

Status code: 422

Result: Passed

Notes: Validation error returned.

## POST /chat empty spaces

Status code: 400

Result: Passed

Notes: API rejected the empty message with a bad request error.
