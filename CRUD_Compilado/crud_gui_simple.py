#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CRUD TIENDA - Versión compilable
Versión simplificada sin dependencias complejas
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox
import json

# Archivo de datos local
DATA_FILE = os.path.join(os.path.dirname(__file__), 'productos.json')

# ======================== DATABASE SIMULADA ========================

def get_productos():
    """Obtiene productos del archivo JSON"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def guardar_productos(productos):
    """Guarda productos en JSON"""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(productos, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Error guardando: {e}")
        return False

def agregar_producto(nombre, descripcion, precio, imagen, stock):
    """Agrega un nuevo producto"""
    if not nombre:
        messagebox.showwarning("Validación", "El nombre es obligatorio")
        return False
    
    productos = get_productos()
    nuevo_id = max([p['id'] for p in productos], default=0) + 1
    
    productos.append({
        'id': nuevo_id,
        'nombre': nombre,
        'descripcion': descripcion,
        'precio': float(precio) if precio else 0,
        'imagen': imagen,
        'stock': int(stock) if stock else 0
    })
    
    if guardar_productos(productos):
        messagebox.showinfo("Éxito", "Producto agregado correctamente")
        return True
    return False

def actualizar_producto(id_prod, nombre, descripcion, precio, imagen, stock):
    """Actualiza un producto"""
    if not nombre:
        messagebox.showwarning("Validación", "El nombre es obligatorio")
        return False
    
    productos = get_productos()
    for p in productos:
        if p['id'] == id_prod:
            p['nombre'] = nombre
            p['descripcion'] = descripcion
            p['precio'] = float(precio) if precio else 0
            p['imagen'] = imagen
            p['stock'] = int(stock) if stock else 0
            break
    
    if guardar_productos(productos):
        messagebox.showinfo("Éxito", "Producto actualizado correctamente")
        return True
    return False

def eliminar_producto(id_prod):
    """Elimina un producto"""
    productos = get_productos()
    productos = [p for p in productos if p['id'] != id_prod]
    
    if guardar_productos(productos):
        messagebox.showinfo("Éxito", "Producto eliminado correctamente")
        return True
    return False

# ======================== GUI ========================

class CRUDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Productos - Tienda")
        self.root.geometry("900x600")
        self.selected_id = None
        
        # Frame principal
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        title_label = ttk.Label(main_frame, text="Gestión de Productos", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # ---- FORMULARIO ----
        form_frame = ttk.LabelFrame(main_frame, text="Datos del Producto", padding="10")
        form_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=10, pady=10)
        
        # Nombre
        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=0, sticky=tk.W)
        self.nombre_entry = ttk.Entry(form_frame, width=30)
        self.nombre_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Descripción
        ttk.Label(form_frame, text="Descripción:").grid(row=1, column=0, sticky=tk.W)
        self.desc_text = tk.Text(form_frame, width=30, height=3)
        self.desc_text.grid(row=1, column=1, padx=5, pady=5)
        
        # Precio
        ttk.Label(form_frame, text="Precio:").grid(row=2, column=0, sticky=tk.W)
        self.precio_entry = ttk.Entry(form_frame, width=30)
        self.precio_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Imagen
        ttk.Label(form_frame, text="Imagen (URL):").grid(row=3, column=0, sticky=tk.W)
        self.imagen_entry = ttk.Entry(form_frame, width=30)
        self.imagen_entry.grid(row=3, column=1, padx=5, pady=5)
        
        # Stock
        ttk.Label(form_frame, text="Stock:").grid(row=4, column=0, sticky=tk.W)
        self.stock_entry = ttk.Entry(form_frame, width=30)
        self.stock_entry.grid(row=4, column=1, padx=5, pady=5)
        self.stock_entry.insert(0, "0")
        
        # Botones
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Agregar", command=self.agregar).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Actualizar", command=self.actualizar).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Eliminar", command=self.eliminar).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Limpiar", command=self.limpiar_form).pack(side=tk.LEFT, padx=5)
        
        # ---- TABLA ----
        table_frame = ttk.LabelFrame(main_frame, text="Lista de Productos", padding="10")
        table_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        
        # Columnas
        self.tree = ttk.Treeview(table_frame, columns=("ID", "Nombre", "Descripción", "Precio", "Stock"), height=12)
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("ID", anchor=tk.W, width=40)
        self.tree.column("Nombre", anchor=tk.W, width=150)
        self.tree.column("Descripción", anchor=tk.W, width=250)
        self.tree.column("Precio", anchor=tk.W, width=80)
        self.tree.column("Stock", anchor=tk.W, width=60)
        
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("ID", text="ID", anchor=tk.W)
        self.tree.heading("Nombre", text="Nombre", anchor=tk.W)
        self.tree.heading("Descripción", text="Descripción", anchor=tk.W)
        self.tree.heading("Precio", text="Precio", anchor=tk.W)
        self.tree.heading("Stock", text="Stock", anchor=tk.W)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        # Cargar datos
        self.refresh_tabla()
    
    def agregar(self):
        """Agrega un nuevo producto"""
        nombre = self.nombre_entry.get()
        descripcion = self.desc_text.get("1.0", tk.END).strip()
        try:
            precio = float(self.precio_entry.get() or 0)
        except ValueError:
            messagebox.showwarning("Validación", "Precio debe ser un número")
            return
        
        imagen = self.imagen_entry.get()
        try:
            stock = int(self.stock_entry.get() or 0)
        except ValueError:
            messagebox.showwarning("Validación", "Stock debe ser un número")
            return
        
        if agregar_producto(nombre, descripcion, precio, imagen, stock):
            self.refresh_tabla()
            self.limpiar_form()
    
    def actualizar(self):
        """Actualiza el producto seleccionado"""
        if not self.selected_id:
            messagebox.showwarning("Selección", "Selecciona un producto para actualizar")
            return
        
        nombre = self.nombre_entry.get()
        descripcion = self.desc_text.get("1.0", tk.END).strip()
        try:
            precio = float(self.precio_entry.get() or 0)
        except ValueError:
            messagebox.showwarning("Validación", "Precio debe ser un número")
            return
        
        imagen = self.imagen_entry.get()
        try:
            stock = int(self.stock_entry.get() or 0)
        except ValueError:
            messagebox.showwarning("Validación", "Stock debe ser un número")
            return
        
        if actualizar_producto(self.selected_id, nombre, descripcion, precio, imagen, stock):
            self.refresh_tabla()
            self.limpiar_form()
    
    def eliminar(self):
        """Elimina el producto seleccionado"""
        if not self.selected_id:
            messagebox.showwarning("Selección", "Selecciona un producto para eliminar")
            return
        
        if messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres eliminar este producto?"):
            if eliminar_producto(self.selected_id):
                self.refresh_tabla()
                self.limpiar_form()
    
    def on_select(self, event):
        """Carga los datos del producto seleccionado"""
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            values = self.tree.item(item, 'values')
            id_prod = int(values[0])
            
            productos = get_productos()
            for p in productos:
                if p['id'] == id_prod:
                    self.selected_id = id_prod
                    self.nombre_entry.delete(0, tk.END)
                    self.nombre_entry.insert(0, p['nombre'])
                    
                    self.desc_text.delete("1.0", tk.END)
                    self.desc_text.insert("1.0", p['descripcion'])
                    
                    self.precio_entry.delete(0, tk.END)
                    self.precio_entry.insert(0, str(p['precio']))
                    
                    self.imagen_entry.delete(0, tk.END)
                    self.imagen_entry.insert(0, p['imagen'])
                    
                    self.stock_entry.delete(0, tk.END)
                    self.stock_entry.insert(0, str(p['stock']))
                    break
    
    def limpiar_form(self):
        """Limpia el formulario"""
        self.nombre_entry.delete(0, tk.END)
        self.desc_text.delete("1.0", tk.END)
        self.precio_entry.delete(0, tk.END)
        self.imagen_entry.delete(0, tk.END)
        self.stock_entry.delete(0, tk.END)
        self.stock_entry.insert(0, "0")
        self.selected_id = None
        self.tree.selection_remove(self.tree.selection())
    
    def refresh_tabla(self):
        """Refresca la tabla de productos"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Cargar productos
        productos = get_productos()
        for p in productos:
            self.tree.insert('', 0, values=(
                p['id'],
                p['nombre'],
                p['descripcion'][:50] if p['descripcion'] else "",
                f"${p['precio']:.2f}",
                p['stock']
            ))

# ======================== MAIN ========================

if __name__ == '__main__':
    root = tk.Tk()
    app = CRUDApp(root)
    root.mainloop()
