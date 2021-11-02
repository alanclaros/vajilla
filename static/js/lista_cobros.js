//imprimir recibo
function listaCobrosImprimir(id) {
    document.forms['form_print'].elements['operation_x'].value = 'mostrar_recibo';
    document.forms['form_print'].elements['id'].value = id;

    document.forms['form_print'].submit();
}