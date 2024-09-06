

airport_iata = r'^[A-Z]{3}$'
airport_icao = r'^[A-Z]{4}$'
airport_code_ru = r'^([А-Я]{3})|.{0}$'
company_iata = r'^[A-Z0-9]{2}$'
airport_iata_many = r'^[A-Z]{3}(,[A-Z]{3})*$'
company_iata_many = r'^[A-Z0-9]{2}(,[A-Z0-9]{2})*$'
relation_alias = r'^((?P<op>\w+)@|(?P<meth>\w+)::)?((?P<relations>\w+)\^)*((?P<clauses>\w+)\~)*((?P<fields>\w+)\.?)+$'
