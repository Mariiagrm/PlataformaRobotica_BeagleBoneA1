#!/bin/bash
#


#----------------------------------------------------------
# Pasar carpeta: scp -r ./SistemasEmpotrados_PlataformaRobotica debian@192.168.7.2:/home/debian/
#----------------------------------------------------------


# Script para habilitar GPIOs y PWMs de la configuración de las ruedas
# Adaptado para un sistema de ficheros tipo /sys/class/gpio y /sys/class/pwm
# (ej. BeagleBone Black u otros Linux embebidos).

set -e  # Opcional: salir si hay cualquier error

GPIO_BASE_DIR="/sys/class/gpio"
PWM_BASE_DIR="/sys/class/pwm"

#----------------------------------------------------------
# Funciones auxiliares
#----------------------------------------------------------

# Exporta un GPIO si no está ya exportado
export_gpio() {
    local gpio_num="$1"
    if [ ! -d "${GPIO_BASE_DIR}/gpio${gpio_num}" ]; then
        echo "${gpio_num}" > "${GPIO_BASE_DIR}/export"
    fi
}

# Configura dirección y valor de un GPIO
set_gpio() {
    local gpio_num="$1"
    local direction="$2"  # "in" o "out"
    local value="$3"      # 0 o 1 (solo si direction=out)

    export_gpio "${gpio_num}"

    local gpio_dir="${GPIO_BASE_DIR}/gpio${gpio_num}"

    echo "${direction}" > "${gpio_dir}/direction"

    if [ "${direction}" = "out" ] && [ -n "${value}" ]; then
        echo "${value}" > "${gpio_dir}/value"
    fi
}

# Configura un PWM dado su directorio (por ejemplo pwm-2:0)
set_pwm() {
    local pwm_dir_name="$1"  # ej: pwm-2:0
    local period="$2"        # en ns normalmente
    local duty="$3"          # en ns normalmente
    local enable="$4"        # 1 o 0

    local pwm_dir="${PWM_BASE_DIR}/${pwm_dir_name}"

    if [ ! -d "${pwm_dir}" ]; then
        echo "Directorio PWM ${pwm_dir} no encontrado. ¿Está exportado?" >&2
        return 1
    fi

    echo "${period}" > "${pwm_dir}/period"
    echo "${duty}" > "${pwm_dir}/duty_cycle"
    echo "${enable}" > "${pwm_dir}/enable"
}

#----------------------------------------------------------
# GPIOs de los encoders (ENTRADAS)
#----------------------------------------------------------

# P9.25 - gpio 5.17 = gpio177 (5*32+17)
set_gpio 177 in

# P9.18 - gpio 6.16 = gpio208 (6*32+16)
set_gpio 208 in

#----------------------------------------------------------
# GPIOs del puente H para control de giro motores (SALIDAS)
#
# Convención:
# A B
# 0 1 --> Hacia adelante
# 1 0 --> Hacia atrás
#----------------------------------------------------------

# --------- Motor 1 -----------
# P8.07 (gpio 5.05 = gpio165) --> A
# P8.08 (gpio 5.06 = gpio166) --> B
# Configuración inicial: atras (A=0, B=1)

set_gpio 165 out 0   # A1 = 0
set_gpio 166 out 1   # B1 = 1

# --------- Motor 2 -----------
# P8.09 (gpio 5.18 = gpio178) --> A
# P8.10 (gpio 5.04 = gpio164) --> B
# Configuración inicial: atras (A=0, B=1)

set_gpio 178 out 0   # A2 = 0
set_gpio 164 out 1   # B2 = 1

#----------------------------------------------------------
# PWMs para control de velocidad
#----------------------------------------------------------
# NOTA IMPORTANTE:
# En muchos sistemas hay que "exportar" el PWM antes, por ejemplo:
#   echo 0 > /sys/class/pwm/pwmchip2/export
#   echo 1 > /sys/class/pwm/pwmchip2/export
# o similar. Adapta esto a tu plataforma concreta.
#----------------------------------------------------------

# Ejemplo:
# P9.14 -> pwm-2:0
# P9.16 -> pwm-2:1
# period = 4000, duty_cycle = 2000, enable = 1

set_pwm "pwm-2:0" 4000 2000 1  # izquierda
set_pwm "pwm-2:1" 4000 2000 1 # derecha

#----------Configurar encoders-------------
#P9.25 - gpio 5.17=gpio177 endocer= derecha
set_gpio 177 in

#P9.18 - gpio 6.16=gpio208 encoder = izquerda
set_gpio 208 in 

#-----------Sensor de ultrasonidos---------------
#P8.36 - gpio 7.10 - gpio234. Señal trigger (out) 
set_gpio 234 out
#P9.17 - gpio 6.17 - gpio209. Señal echo (in)
set_gpio 209 in



echo "Configuración de GPIOs y PWMs de ruedas completada."
