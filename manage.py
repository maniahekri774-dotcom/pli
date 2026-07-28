"""CLI management commands: seed database, create admin user, etc."""

import os
import click
from dotenv import load_dotenv

load_dotenv()

from app import create_app
from app.extensions import db
from app.models import User, Role

app = create_app(os.environ.get("FLASK_ENV", "development"))


@app.cli.command("seed-roles")
def seed_roles():
    """Create default roles if they don't exist."""
    defaults = ["student", "teacher", "admin", "super_admin"]
    for name in defaults:
        if not Role.query.filter_by(name=name).first():
            db.session.add(Role(name=name))
    db.session.commit()
    click.echo("Roles seeded.")


@app.cli.command("create-admin")
@click.option("--email", prompt=True)
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
@click.option("--first-name", prompt=True)
@click.option("--last-name", prompt=True)
def create_admin(email, password, first_name, last_name):
    """Create a super_admin user."""
    role = Role.query.filter_by(name="super_admin").first()
    if not role:
        click.echo("Run 'flask seed-roles' first.")
        return

    if User.query.filter_by(email=email).first():
        click.echo("User already exists.")
        return

    user = User(
        email=email,
        first_name=first_name,
        last_name=last_name,
        role=role,
        is_active=True,
        is_email_verified=True,
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    click.echo(f"Admin user {email} created.")


if __name__ == "__main__":
    app.run()
