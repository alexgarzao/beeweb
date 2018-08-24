@then(u'os arquivos são')
def step_impl(context):
    for row in context.table:
        file_id = row['identificação']
        filename = row['arquivo']
        context.config.driver.add_file(file_id, filename)
