from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = 'clave_segura_equipo2'

# Almacenamiento temporal
clientes = []
pedidos = []

# Imagen por defecto
@app.template_filter('imagen_perfil')
def imagen_perfil(url):
    if url and url.strip():
        return url
    return 'https://cdn-icons-png.flaticon.com/512/149/149071.png'

# ------------------- CLIENTES -------------------
@app.route('/', methods=['GET', 'POST'])
def registro_clientes():
    cliente_editar = None
    
    # Cargar cliente para editar
    if request.args.get('editar_id'):
        editar_id = int(request.args.get('editar_id'))
        for c in clientes:
            if c['id'] == editar_id:
                cliente_editar = c
    
    if request.method == 'POST':
        accion = request.form.get('accion')
        
        if accion == 'agregar':
            nombre = request.form.get('nombre')
            correo = request.form.get('correo')
            telefono = request.form.get('telefono')
            direccion = request.form.get('direccion')
            imagen = request.form.get('imagen') or ''

            if not nombre or not correo or not telefono:
                flash('Faltan campos obligatorios', 'error')
            else:
                cliente = {
                    'id': len(clientes) + 1,
                    'nombre': nombre,
                    'correo': correo,
                    'telefono': telefono,
                    'direccion': direccion,
                    'imagen': imagen
                }
                clientes.append(cliente)
                flash('Cliente agregado', 'exito')
        
        elif accion == 'editar':
            cliente_id = int(request.form.get('id_cliente'))
            for c in clientes:
                if c['id'] == cliente_id:
                    c['nombre'] = request.form.get('nombre')
                    c['correo'] = request.form.get('correo')
                    c['telefono'] = request.form.get('telefono')
                    c['direccion'] = request.form.get('direccion')
                    nueva_imagen = request.form.get('imagen')
                    if nueva_imagen:
                        c['imagen'] = nueva_imagen
                    flash('Cliente actualizado', 'exito')
                    break
        
        return redirect(url_for('registro_clientes'))
    
    return render_template('registro_clientes.html', clientes=clientes, editar=cliente_editar)

@app.route('/eliminar-cliente/<int:cliente_id>')
def eliminar_cliente(cliente_id):
    global clientes
    clientes = [c for c in clientes if c['id'] != cliente_id]
    flash('Cliente eliminado', 'exito')
    return redirect(url_for('registro_clientes'))

# ------------------- PEDIDOS -------------------
@app.route('/pedido-alimentos', methods=['GET', 'POST'])
def pedido_alimentos():
    pedido_editar = None
    
    # Cargar pedido para editar
    if request.args.get('editar_id'):
        editar_id = int(request.args.get('editar_id'))
        for p in pedidos:
            if p['id'] == editar_id:
                pedido_editar = p
    
    if request.method == 'POST':
        accion = request.form.get('accion')
        
        if accion == 'agregar':
            nombre_cliente = request.form.get('nombre_cliente')
            alimento = request.form.get('alimento')
            cantidad = request.form.get('cantidad')
            observaciones = request.form.get('observaciones')
            imagen = request.form.get('imagen') or ''

            if not nombre_cliente or not alimento or not cantidad:
                flash('Faltan campos obligatorios', 'error')
            else:
                pedido = {
                    'id': len(pedidos) + 1,
                    'nombre_cliente': nombre_cliente,
                    'alimento': alimento,
                    'cantidad': cantidad,
                    'observaciones': observaciones,
                    'imagen': imagen
                }
                pedidos.append(pedido)
                flash('Pedido agregado', 'exito')
        
        elif accion == 'editar':
            pedido_id = int(request.form.get('id_pedido'))
            for p in pedidos:
                if p['id'] == pedido_id:
                    p['nombre_cliente'] = request.form.get('nombre_cliente')
                    p['alimento'] = request.form.get('alimento')
                    p['cantidad'] = request.form.get('cantidad')
                    p['observaciones'] = request.form.get('observaciones')
                    nueva_imagen = request.form.get('imagen')
                    if nueva_imagen:
                        p['imagen'] = nueva_imagen
                    flash('Pedido actualizado', 'exito')
                    break
        
        return redirect(url_for('pedido_alimentos'))
    
    return render_template('pedido_alimentos.html', pedidos=pedidos, editar=pedido_editar)

@app.route('/eliminar-pedido/<int:pedido_id>')
def eliminar_pedido(pedido_id):
    global pedidos
    pedidos = [p for p in pedidos if p['id'] != pedido_id]
    flash('Pedido eliminado', 'exito')
    return redirect(url_for('pedido_alimentos'))

if __name__ == '__main__':
    app.run(debug=True)