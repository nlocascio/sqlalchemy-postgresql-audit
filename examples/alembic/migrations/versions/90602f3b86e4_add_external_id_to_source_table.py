"""Add external_id to source table

Revision ID: 90602f3b86e4
Revises: 33d56e6de360
Create Date: 2019-06-23 12:28:18.310158

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90602f3b86e4'
down_revision = '33d56e6de360'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('test', sa.Column('external_id', sa.Integer(), nullable=False))
    op.add_column('test_audit', sa.Column('external_id', sa.Integer(), nullable=True))
    op.execute("CREATE OR REPLACE FUNCTION public_test_audit() RETURNS TRIGGER AS $public_test_audit$\nBEGIN\n    IF current_setting('audit.username', false)::VARCHAR::VARCHAR = '' THEN RAISE EXCEPTION 'audit.username session setting must be set to a non null/empty value'; END IF;\n\n    IF (TG_OP = 'DELETE') THEN\n        INSERT INTO test_audit (audit_operation, audit_operation_timestamp, audit_current_user, audit_username, id, name, external_id) SELECT 'D', now(), current_user, current_setting('audit.username', false)::VARCHAR, OLD.id, OLD.name, OLD.external_id;\n    ELSIF (TG_OP = 'UPDATE') THEN\n        INSERT INTO test_audit (audit_operation, audit_operation_timestamp, audit_current_user, audit_username, id, name, external_id) SELECT 'U', now(), current_user, current_setting('audit.username', false)::VARCHAR, NEW.id, NEW.name, NEW.external_id;\n    ELSIF (TG_OP = 'INSERT') THEN\n        INSERT INTO test_audit (audit_operation, audit_operation_timestamp, audit_current_user, audit_username, id, name, external_id) SELECT 'I', now(), current_user, current_setting('audit.username', false)::VARCHAR, NEW.id, NEW.name, NEW.external_id;\n    END IF;\n    RETURN NULL; -- result is ignored since this is an AFTER trigger\nEND;\n$public_test_audit$ LANGUAGE plpgsql;\n\nDROP TRIGGER IF EXISTS public_test_audit ON test;\n\nCREATE TRIGGER public_test_audit\nAFTER INSERT OR UPDATE OR DELETE ON test\nFOR EACH ROW EXECUTE PROCEDURE public_test_audit();\n")
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('DROP TRIGGER IF EXISTS public_test_audit ON test;\nDROP FUNCTION IF EXISTS public_test_audit;\n')
    op.drop_column('test_audit', 'external_id')
    op.drop_column('test', 'external_id')
    # ### end Alembic commands ###