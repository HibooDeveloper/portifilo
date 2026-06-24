"""manage.py — CLI commands for database and admin management"""
import click
import os
from flask.cli import FlaskGroup
from app import create_app, db

app = create_app()
cli = FlaskGroup(create_app=lambda: app)


@cli.command('db-init')
def db_init():
    """Create all database tables (safe to run multiple times)."""
    with app.app_context():
        # Try Flask-Migrate first, fall back to create_all
        try:
            from flask_migrate import upgrade, stamp
            # Check if migrations directory exists
            if os.path.isdir(os.path.join(app.root_path, '..', 'migrations')):
                upgrade()
                click.echo('✓ Database migrated (Alembic)')
            else:
                db.create_all()
                click.echo('✓ Database tables created (create_all)')
        except ImportError:
            db.create_all()
            click.echo('✓ Database tables created (create_all)')


@cli.command('create-admin')
@click.option('--name', prompt='Admin name')
@click.option('--email', prompt='Admin email')
@click.option('--password', prompt=True, hide_input=True,
              confirmation_prompt=True)
def create_admin(name, email, password):
    """Create a super admin user."""
    from app.models import User
    with app.app_context():
        if User.query.filter_by(email=email).first():
            click.echo('⚠  Email already exists. Skipping.')
            return
        u = User(
            name=name, email=email, role='super_admin',
            is_active=True, is_verified=True
        )
        u.set_password(password)
        db.session.add(u)
        db.session.commit()
        click.echo(f'✓ Super admin created: {email}')


@cli.command('seed')
@click.option('--with-admin/--no-admin', default=True)
def seed(with_admin):
    """Seed the database with sample data for development."""
    from app.models import User, Project, Service, Testimonial, BlogPost
    import json

    with app.app_context():
        # Admin user
        if with_admin and not User.query.filter_by(email='admin@abubaker.dev').first():
            u = User(name='Abubaker Admin', email='admin@abubaker.dev',
                     role='super_admin', is_active=True, is_verified=True)
            u.set_password('admin123')
            db.session.add(u)

        # Sample services
        if Service.query.count() == 0:
            services = [
                Service(icon='📱', title_ar='تطبيقات الجوال', title_en='Mobile Apps',
                        desc_ar='تطوير تطبيقات iOS و Android', desc_en='iOS & Android development',
                        tags=json.dumps(['flutter', 'dart']), sort_order=1),
                Service(icon='🌐', title_ar='مواقع الويب', title_en='Web Development',
                        desc_ar='تطوير مواقع متكاملة', desc_en='Full-stack web development',
                        tags=json.dumps(['react', 'python']), sort_order=2),
                Service(icon='🤖', title_ar='حلول الذكاء الاصطناعي', title_en='AI Solutions',
                        desc_ar='تطوير حلول ذكاء اصطناعي', desc_en='AI-powered solutions',
                        tags=json.dumps(['python', 'tensorflow']), sort_order=3),
            ]
            db.session.add_all(services)
            click.echo('✓ Sample services created')

        # Sample testimonial
        if Testimonial.query.count() == 0:
            t = Testimonial(
                client_name='Ahmed Hassan',
                client_role_ar='مدير تقني', client_role_en='CTO',
                text_ar='عمل ممتاز وتسليم في الوقت المحدد',
                text_en='Excellent work and on-time delivery',
                rating=5, sort_order=1
            )
            db.session.add(t)
            click.echo('✓ Sample testimonial created')

        db.session.commit()
        if with_admin:
            click.echo('✓ Admin user: admin@abubaker.dev / admin123')
        click.echo('✓ Seed complete')


if __name__ == '__main__':
    cli()
