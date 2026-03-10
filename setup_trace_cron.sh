#!/bin/bash
(crontab -l 2>/dev/null; echo "*/10 * * * * cd /config && ./upload_traces.sh >> /config/upload_traces.log 2>&1") | crontab -
echo "Cron job installed. Verify with: crontab -l"
