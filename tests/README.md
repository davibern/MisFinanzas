# Guía de Tests Unitarios

Esta carpeta contiene los tests unitarios del proyecto MisFinanzas.

## 📚 ¿Qué son los tests unitarios?

Los tests unitarios son pruebas automáticas que verifican que cada "unidad" de código (función, método, clase) funciona correctamente de forma aislada.

## 🎯 Conceptos clave

### 1. **Fixtures** (`@pytest.fixture`)
Son funciones que preparan datos o configuración que necesitan los tests. Se ejecutan antes de cada test que las use.

```python
@pytest.fixture
def datos_prueba():
    return pd.DataFrame({...})  # Datos de ejemplo
```

### 2. **Mocks** (`@patch`, `MagicMock`)
Simulan dependencias externas (archivos, bases de datos, APIs) para que los tests no dependan de recursos reales.

```python
with patch('pandas.read_parquet', return_value=datos_prueba):
    finanzas = MisFinanzas()  # Usa datos_prueba en vez del archivo real
```

### 3. **Assertions** (`assert`)
Verifican que el resultado de una función sea el esperado. Si falla, el test falla.

```python
assert resultado == 2500.0, "El resultado debería ser 2500.0"
```

### 4. **Patrón AAA**
- **Arrange** (Preparar): Configurar datos y estado inicial
- **Act** (Actuar): Ejecutar la función a probar
- **Assert** (Verificar): Comprobar que el resultado es correcto

## 🚀 Cómo ejecutar los tests

### Instalar pytest (si no lo tienes)
```bash
pip install pytest pytest-cov
```

### Ejecutar todos los tests
```bash
pytest
```

### Ejecutar tests con más detalle
```bash
pytest -v
```

### Ejecutar un test específico
```bash
pytest tests/test_mis_finanzas.py::test_obtener_ingresos_mes_año
```

### Ver cobertura de código
```bash
pytest --cov=src tests/
```

## 📝 Estructura de un test

```python
def test_nombre_descriptivo(fixture_si_necesario):
    """Descripción de qué prueba este test"""
    
    # Arrange: Preparar datos (si no viene del fixture)
    dato_entrada = 123
    
    # Act: Ejecutar la función
    resultado = funcion_a_probar(dato_entrada)
    
    # Assert: Verificar resultado
    assert resultado == valor_esperado
```

## 💡 Buenas prácticas

1. **Nombres descriptivos**: El nombre del test debe explicar qué prueba
   - ✅ `test_obtener_ingresos_mes_año`
   - ❌ `test_1`

2. **Un concepto por test**: Cada test debe probar una sola cosa

3. **Tests independientes**: Un test no debe depender de otro

4. **Casos límite**: Prueba casos normales y casos extremos (valores vacíos, negativos, etc.)

5. **Mensajes claros**: Usa mensajes descriptivos en los asserts
   ```python
   assert resultado == 100, f"Se esperaba 100 pero se obtuvo {resultado}"
   ```
