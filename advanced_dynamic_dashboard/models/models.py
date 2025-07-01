
from odoo import models
from odoo.models import BaseModel
def get_query(self, args, operation, field, group_by=False,
              apply_ir_rules=False):
    """Method for creating query for fetching data to be displayed on the
    dashboard block"""
    query = self._where_calc(args)

    if apply_ir_rules:
        self._apply_ir_rules(query, 'read')

    join = ''
    group_by_str = ''


    if operation and field:
        data = 'COALESCE(%s("%s".%s),0) AS value' % (operation.upper(),
                                                     self._table, field.name)
        if group_by:
            if group_by.ttype == 'many2one':
                relation_model = group_by.relation.replace('.', '_')
                join = ' INNER JOIN %s on "%s".id = "%s".%s' % (
                    relation_model, relation_model, self._table, group_by.name)
                rec_name = self.env[group_by.relation]._rec_name_fallback()
                data = data + ',"%s".%s AS %s' % (relation_model, rec_name,
                                                  group_by.name)
                group_by_str = ' Group by "%s".%s' % (relation_model, rec_name)
            else:
                data = data + ',"%s".%s' % (self._table, group_by.name)
                group_by_str = ' Group by "%s".%s' % (self._table,
                                                      str(group_by.name))
    else:
        data = '"%s".id' % self._table
    from_clause, where_clause, where_clause_params = query.get_sql()
    where_str = where_clause and (" WHERE %s" % where_clause) or ''
    query_str = ('SELECT %s FROM ' % data + from_clause + join + where_str +
                 group_by_str)
    return query_str % tuple(
        map(lambda x: "'" + str(x) + "'", where_clause_params))

models.BaseModel.get_query = get_query
