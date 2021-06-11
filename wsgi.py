"""Start the application."""

import click
from nbaspa_app import create_app

@click.command()
@click.option(
    "--config",
    type=click.Choice(["development", "production"], case_sensitive=True),
    default="development",
    help="Whether to launch the application with the production configuration"
)
@click.option(
    "--host", type=str, default="0.0.0.0", help="The host to launch the application on"
)
@click.option(
    "--port", type=str, default="8000", help="The port to launch the application on"
)
def main(config, host, port):
    """Launch the application."""
    app = create_app(config=config)
    app.run(host=host, port=port)

if __name__ == "__main__":
    main()
