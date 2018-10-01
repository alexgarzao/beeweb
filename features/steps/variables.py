from behave import given, when, then

from features.support.simple_result import SimpleResult


@given(u'que quero definir variáveis')  # noqa: F811
def step_impl(context):
    pass


@given(u'que quero consultar o valor de {variable}')  # noqa: F811
@when(u'consulto o valor de {variable}')
def step_impl(context, variable):
    context.variable_result = context.module.get_variable_result(variable)


@then(u'defino que {variable} igual a {value}')  # noqa: F811
@when(u'defino que {variable} igual a {value}')  # noqa: F811
def step_impl(context, variable, value):
    value = context.module.get_content(value)
    context.module.set_variable_result(variable, SimpleResult(value))


@then(u'obtenho o valor {expected_value}')  # noqa: F811
def step_impl(context, expected_value):
    valor_variavel = context.variable_result
    assert valor_variavel == expected_value, \
        "O resultado esperado [%s] e diferente do retorno [%s]." % (expected_value, valor_variavel)


@given(u'que {variable} = {value}')  # noqa: F811
def step_impl(context, variable, value):
    value = context.module.get_content(value)
    context.module.set_variable_result(variable, SimpleResult(value))
