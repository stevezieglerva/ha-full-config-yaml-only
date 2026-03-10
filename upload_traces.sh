#!/bin/bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
/usr/local/bin/aws s3 cp ../homeassistant/.storage/trace.saved_traces "s3://svz-home-assistant/traces/trace.saved_traces_${TIMESTAMP}"
