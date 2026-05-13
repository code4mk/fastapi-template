"""Seed users for local development."""

from sqlalchemy.orm import Session

from app.models.users import User
from fastapi_pundra.common.seeder import BaseSeeder
from app.seeders.factories import UserFactory, random_plain_password
from fastapi_pundra.common.password import generate_password_hash


class UserSeeder(BaseSeeder):
    """Seed the users table with sample accounts."""

    name = "UserSeeder"
    order = 10
    count = 10

    def should_seed(self, session: Session) -> bool:
        """Skip if users already exist."""
        return session.query(User).count() == 0

    def run(self, session: Session) -> None:
        """Create an admin user and random sample users."""
        admin_plain = random_plain_password()
        admin = UserFactory.build(
            name="Admin User",
            email="admin@nexus.local",
            status="active",
            password=generate_password_hash(admin_plain),
        )
        session.add(admin)

        users = UserFactory.build_batch(self.count - 1)
        session.add_all(users)

        session.flush()
        print(  # noqa: T201
            f"  Created {self.count} users (login: admin@nexus.local / {admin_plain})"
        )
