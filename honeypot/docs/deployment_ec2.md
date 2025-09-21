# EC2 Deployment Notes

1. Launch Ubuntu 22.04 instance.
2. Open port 22 for admin SSH and 2222 for the honeypot (restrict 22 by IP).
3. Clone repo, run `./provision.sh` (optional), then `./start.sh`.
4. Monitor: `docker logs -f cowrie` and `tail -F cowrie/data/log/cowrie.session.log`.
5. Rotate logs or forward to S3/ELK for analysis in production.
