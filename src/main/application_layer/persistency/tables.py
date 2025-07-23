from sqlalchemy.sql import func
from uuid import UUID

from main.app import db

address_table = db.Table(
    'addresses', db.metadata,
    db.Column('uuid',
              db.Uuid(as_uuid=True),
              unique=True, nullable=False, primary_key=True),
    db.Column('address', db.String(100), unique=True, nullable=False),
    db.Column('private_key', db.String, nullable=False),
    db.Column('insert_at', db.DateTime(timezone=True), server_default=func.now()),
)

transaction_table = db.Table(
    'transactions', db.metadata,
    db.Column('uuid',
              db.Uuid(as_uuid=True),
              unique=True, nullable=False, primary_key=True),
    db.Column('tx_hash', db.String(100), unique=True, nullable=False),
    db.Column('asset', db.String(10), nullable=False),
    db.Column('to_address', db.String(100), nullable=False),
    db.Column('value', db.Float(asdecimal=True), nullable=False),
    db.Column('insert_at', db.DateTime(timezone=True), server_default=func.now()),
)       


transfer_table = db.Table(
    'transfers', db.metadata,
    db.Column('uuid',
              db.Uuid(as_uuid=True),
              unique=True, nullable=False, primary_key=True),
    db.Column('tx_hash', db.String(100), unique=True, nullable=False),
    db.Column('from_address', db.String(100), nullable=False),
    db.Column('to_address', db.String(100), nullable=False),
    db.Column('asset', db.String(10), nullable=False),
    db.Column('value', db.Float(asdecimal=True), nullable=False),
    db.Column('status', db.String(10), nullable=False),
    db.Column('gas_used', db.Float(asdecimal=True), nullable=False),
    db.Column('gas_price', db.Float(asdecimal=True), nullable=False),
    db.Column('insert_at', db.DateTime(timezone=True), server_default=func.now()),
)   
