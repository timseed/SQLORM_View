
from db import engine, Meta

from sqlalchemy import Column, Table, MetaData, event
from sqlalchemy.ext import compiler
from sqlalchemy.schema import DDLElement, PrimaryKeyConstraint, DDL


class CreateView(DDLElement):
    def __init__(self, name, selectable):
        self.name = name
        self.selectable = selectable
        print("CreateView called")
        engine.execute(self)


@compiler.compiles(CreateView)
def compile(element, compiler, **kw):
    # Could use "CREATE OR REPLACE MATERIALIZED VIEW..."
    # but I'd rather have noisy errors
    print("Compiler fired")
    return 'CREATE VIEW %s AS %s' % (
        element.name,
        compiler.sql_compiler.process(element.selectable, literal_binds=True),
    )


def f(name, selectable):
    print("f Called")


def create_view(name, selectable, metadata=Meta):
    _mt = MetaData()  # temp metadata just for initial Table object creation
    t = Table(name, metadata)  # the actual mat view class is bound to metadata
    for c in selectable.c:
        t.append_column(Column(c.name, c.type, primary_key=True))
        print(f"View {name} adding Col {c.name}")

    if not (any([c.primary_key for c in selectable.c])):
        t.append_constraint(PrimaryKeyConstraint(*[c.name for c in selectable.c]))
        print(f"Adding PK Constraint {c.name}")

    event.listen(
        metadata, 'after_create',
        CreateView(name, selectable)
    )

    @event.listens_for(metadata, 'after_create')
    def create_indexes(target, connection, **kw):
        print("After Create Fired")
        for idx in t.indexes:
            print("Creating Index")
            idx.create(connection)

    event.listen(
        metadata, 'before_drop',
        DDL('DROP VIEW IF EXISTS ' + name)
    )

    return t
