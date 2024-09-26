import numpy as np
import matplotlib.pyplot as plt
import ephem
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry

def get_moon_phase(date=None):
    # Si no se proporciona una fecha, usa la actual
    if date is None:
        now = datetime.now()
    else:
        now = datetime.strptime(date, "%Y-%m-%d")
        now = now.replace(hour=12, minute=0, second=0)  # Configura la hora a las 12:00

    date_str = now.strftime("%Y-%m-%d %H:%M:%S")
    
    # Extrae detalles de la fecha
    day = now.day
    month = now.strftime("%B")
    year = now.year
    hour = now.strftime("%H:%M:%S")
    
    # Calcula la fase lunar
    moon = ephem.Moon()
    observer = ephem.Observer()
    observer.date = now
    moon.compute(observer)

    # Determina la fase lunar
    phase = moon.phase  # Fase lunar en grados
    phase_name = ''
    
    if phase < 1:
        phase_name = 'Nueva'
    elif phase < 49:
        phase_name = 'Creciente'
    elif phase < 51:
        phase_name = 'Llena'
    else:
        phase_name = 'Menguante'
    
    return phase_name, phase, date_str, day, month, year, hour

def draw_moon_phase(phase, day, month, year, hour):
    # Dibuja la fase de la luna con diseño atractivo
    fig, ax = plt.subplots(figsize=(6, 6))  # Tamaño aumentado
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    
    # Color oscuro para fondo igual que el círculo de la luna
    dark_color = '#001f3f'  # Color oscuro para simular la noche

    # Establece el color del fondo del canvas y el gráfico
    fig.patch.set_facecolor(dark_color)
    ax.set_facecolor(dark_color)

    # Crea un círculo para la luna
    moon_circle = plt.Circle((0, 0), 0.5, color='#FFEB3B', zorder=1, edgecolor='gold', linewidth=2)  # Color amarillo suave y borde dorado

    # Crea el sombreado según la fase lunar
    if phase == 'Nueva':
        ax.add_artist(moon_circle)
    elif phase == 'Creciente':
        crescent = plt.Circle((0.2, 0), 0.5, color=dark_color, zorder=2)  # Color del fondo
        ax.add_artist(moon_circle)
        ax.add_artist(crescent)
    elif phase == 'Llena':
        ax.add_artist(moon_circle)
    elif phase == 'Menguante':
        crescent = plt.Circle((-0.2, 0), 0.5, color=dark_color, zorder=2)  # Color del fondo
        ax.add_artist(moon_circle)
        ax.add_artist(crescent)

    ax.set_aspect('equal')
    ax.axis('off')  # Oculta los ejes
    plt.title(f"Fase de la Luna: {phase}", fontsize=16, color='white', fontweight='bold', family='sans-serif')

    # Información organizada con sombras y esquinas redondeadas
    ax.text(0, -0.8, f"Fecha: {day} {month} {year}", ha='center', fontsize=12, color='white', fontweight='light')
    ax.text(0, -0.9, f"Hora: {hour}", ha='center', fontsize=12, color='white', fontweight='light')

    # Añadir una sombra al texto
    ax.text(0, -0.8, f"Fecha: {day} {month} {year}", ha='center', fontsize=12, color='black', alpha=0.5, fontweight='light', zorder=0)
    ax.text(0, -0.9, f"Hora: {hour}", ha='center', fontsize=12, color='black', alpha=0.5, fontweight='light', zorder=0)

    # Añadir un toque decorativo
    ax.plot([-1, 1], [1, 1], color='white', linewidth=3)  # Línea decorativa en la parte superior

    plt.show()

def moon_phase_info(phase):
    info = {
        'Nueva': "La luna nueva es el inicio del ciclo lunar. Es un buen momento para iniciar nuevos proyectos.",
        'Creciente': "La luna creciente simboliza el crecimiento y la expansión. Es un buen momento para hacer planes y avanzar en proyectos.",
        'Llena': "La luna llena representa la culminación y la plenitud. Es un buen momento para reflexionar y agradecer.",
        'Menguante': "La luna menguante es un tiempo de liberación y finalización. Es un buen momento para dejar ir lo que ya no sirve."
    }
    return info.get(phase, "Fase lunar desconocida.")

def season(month):
    if month in ["December", "January", "February"]:
        return "Invierno"
    elif month in ["March", "April", "May"]:
        return "Primavera"
    elif month in ["June", "July", "August"]:
        return "Verano"
    else:
        return "Otoño"

# Función que se llamará al seleccionar una nueva fecha
def on_date_change(selected_date):
    global result_label  # Asegura que result_label sea global para ser accesible en esta función
    phase_name, phase_degree, date_str, day, month, year, hour = get_moon_phase(selected_date)
    current_season = season(month)
    
    result_label.config(text=f"Fecha: {day} {month} {year}, Hora: {hour}\nFase lunar: {phase_name} (Grados: {phase_degree:.2f})\nEstación: {current_season}")
    draw_moon_phase(phase_name, day, month, year, hour)

def main():
    global result_label  # Asegura que result_label sea accesible en todo el programa
    root = tk.Tk()
    root.title("Fase Lunar")
    
    # Obtener la fase lunar para hoy al iniciar
    phase_name, phase_degree, date_str, day, month, year, hour = get_moon_phase()
    current_season = season(month)

    # Frame para mostrar la información de la luna
    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

    # Mostrar la información de la fecha actual
    ttk.Label(frame, text="Fecha actual:").grid(column=0, row=0, sticky=tk.W)
    result_label = ttk.Label(frame, text=f"Fecha: {day} {month} {year}, Hora: {hour}\nFase lunar: {phase_name} (Grados: {phase_degree:.2f})\nEstación: {current_season}")
    result_label.grid(column=1, row=0, sticky=tk.W)

    # Selector de fecha
    ttk.Label(frame, text="Seleccionar fecha:").grid(column=0, row=1, sticky=tk.W)
    date_entry = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='y-mm-dd')
    date_entry.grid(column=1, row=1, sticky=tk.W)

    # Botón para calcular la fase lunar de la fecha seleccionada
    calc_button = ttk.Button(frame, text="Mostrar Fase Lunar", command=lambda: on_date_change(date_entry.get_date().strftime('%Y-%m-%d')))
    calc_button.grid(column=2, row=1, sticky=tk.W)

    # Mostrar la fase lunar inicial (hoy)
    draw_moon_phase(phase_name, day, month, year, hour)

    root.mainloop()

if __name__ == "__main__":
    main()
