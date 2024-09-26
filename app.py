import numpy as np
import matplotlib.pyplot as plt
import ephem
from datetime import datetime, timedelta

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

def main():
    while True:
        # Solicita al usuario si desea ingresar una fecha
        user_input = input("Ingrese una fecha (YYYY-MM-DD) o presione Enter para usar la fecha actual: ").strip()

        if user_input == '':
            # Usa la fecha actual
            phase_name, phase_degree, date_str, day, month, year, hour = get_moon_phase()
        else:
            try:
                # Verifica si el formato es correcto
                datetime.strptime(user_input, "%Y-%m-%d")
                # Usa la fecha proporcionada
                phase_name, phase_degree, date_str, day, month, year, hour = get_moon_phase(user_input)
            except ValueError:
                print("Formato de fecha inválido. Intente de nuevo.")
                continue
        
        current_season = season(month)
        
        print(f"\nFecha y hora: {date_str}")
        print(f"Fase lunar: {phase_name} (Grados: {phase_degree:.2f})")
        print(f"Día: {day}, Mes: {month}, Año: {year}, Hora: {hour}, Estación: {current_season}")
        print(moon_phase_info(phase_name))
        
        draw_moon_phase(phase_name, day, month, year, hour)

if __name__ == "__main__":
    main()
