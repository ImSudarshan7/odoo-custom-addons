
from odoo import models
# file: dashboard_patch.py (or inside __init__.py or models/__init__.py)
from odoo.models import BaseModel

def get_query(self, args, operation, field, group_by=False, apply_ir_rules=False):
    query = self._where_calc(args)

    if apply_ir_rules:
        self._apply_ir_rules(query, 'read')

    join = ''
    group_by_str = ''

    if operation and field:
        data = 'COALESCE(%s("%s".%s),0) AS value' % (
            operation.upper(), self._table, field.name)
        if group_by:
            if group_by.ttype == 'many2one':
                relation_model = group_by.relation.replace('.', '_')
                join = ' INNER JOIN %s on "%s".id = "%s".%s' % (
                    relation_model, relation_model, self._table, group_by.name)
                rec_name = self.env[group_by.relation]._rec_name_fallback()
                data += ', "%s".%s AS name' % (relation_model, rec_name)
                group_by_str = ' GROUP BY "%s".%s' % (relation_model, rec_name)
            else:
                data += ', "%s".%s AS name' % (self._table, group_by.name)
                group_by_str = ' GROUP BY "%s".%s' % (self._table, group_by.name)
    else:
        data = '"%s".id' % self._table

    from_clause, where_clause, where_clause_params = query.get_sql()
    where_str = (" WHERE %s" % where_clause) if where_clause else ''
    sql = 'SELECT %s FROM %s%s%s%s' % (
        data, from_clause, join, where_str, group_by_str
    )
    return sql, tuple(where_clause_params)

# Attach to BaseModel class
BaseModel.get_query = get_query
