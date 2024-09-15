# Price Watch

Watch Price for V-Server and send E-Mail if it's 1,- €

## Usage

just pull the latest docker-image
```bash
docker pull mjkatweb/pricewatch

```
and 

### set this env-vars

#### Config for the Mailer

- SMTP_HOST
- SMTP_USER
- SMTP_PASSWORD
- MAIL_FROM
- MAIL_TO

#### Config for the watcher

- INTERVAL (interval in days to do price-checks)
- HARD_LIMIT

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[GNU General Public License v2.0](https://choosealicense.com/licenses/gpl-2.0/)
