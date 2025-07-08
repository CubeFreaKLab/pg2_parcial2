import threading
from datetime import datetime
from typing import List, Dict

class LoggerSingleton:
    """
    Singleton para mantener un registro centralizado de logs del sistema
    Implementación thread-safe
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """Asegura que solo exista una instancia del logger"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._inicializar()
        return cls._instance
    
    def _inicializar(self):
        """Inicializa el logger (solo se ejecuta una vez)"""
        self._logs = []
        self._operaciones_contador = {
            'precio_final': 0,
            'ingredientes_finales': 0,
            'creacion_cono': 0,
            'personalizacion': 0
        }
        self._lock_logs = threading.Lock()
    
    def registrar_operacion(self, tipo_operacion: str, detalle: str, datos_extra: Dict = None):
        """
        Registra una operación en el log
        
        Args:
            tipo_operacion (str): Tipo de operación realizada
            detalle (str): Descripción detallada de la operación
            datos_extra (dict): Datos adicionales de la operación
        """
        with self._lock_logs:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_entry = {
                'timestamp': timestamp,
                'tipo_operacion': tipo_operacion,
                'detalle': detalle,
                'datos_extra': datos_extra or {}
            }
            self._logs.append(log_entry)
            
            # Incrementar contador
            if tipo_operacion in self._operaciones_contador:
                self._operaciones_contador[tipo_operacion] += 1
    
    def obtener_logs(self, limite: int = None) -> List[Dict]:
        """
        Obtiene los logs registrados
        
        Args:
            limite (int): Número máximo de logs a retornar
        
        Returns:
            List[Dict]: Lista de logs
        """
        with self._lock_logs:
            if limite:
                return self._logs[-limite:]
            return self._logs.copy()
    
    def obtener_estadisticas(self) -> Dict:
        """
        Obtiene estadísticas de las operaciones registradas
        
        Returns:
            Dict: Estadísticas del sistema
        """
        with self._lock_logs:
            return {
                'total_logs': len(self._logs),
                'operaciones_por_tipo': self._operaciones_contador.copy(),
                'ultimo_log': self._logs[-1] if self._logs else None
            }
    
    def limpiar_logs(self):
        """Limpia todos los logs registrados"""
        with self._lock_logs:
            self._logs.clear()
            self._operaciones_contador = {
                'precio_final': 0,
                'ingredientes_finales': 0,
                'creacion_cono': 0,
                'personalizacion': 0
            }
    
    def obtener_logs_por_tipo(self, tipo_operacion: str) -> List[Dict]:
        """
        Obtiene logs filtrados por tipo de operación
        
        Args:
            tipo_operacion (str): Tipo de operación a filtrar
        
        Returns:
            List[Dict]: Logs filtrados
        """
        with self._lock_logs:
            return [log for log in self._logs if log['tipo_operacion'] == tipo_operacion]
    
    def obtener_logs_recientes(self, minutos: int = 60) -> List[Dict]:
        """
        Obtiene logs de los últimos N minutos
        
        Args:
            minutos (int): Número de minutos hacia atrás
        
        Returns:
            List[Dict]: Logs recientes
        """
        with self._lock_logs:
            from datetime import datetime, timedelta
            limite_tiempo = datetime.now() - timedelta(minutes=minutos)
            
            logs_recientes = []
            for log in self._logs:
                log_time = datetime.strptime(log['timestamp'], '%Y-%m-%d %H:%M:%S')
                if log_time >= limite_tiempo:
                    logs_recientes.append(log)
            
            return logs_recientes

# Función de conveniencia para obtener la instancia del logger
def obtener_logger():
    """
    Función de conveniencia para obtener la instancia del logger
    
    Returns:
        LoggerSingleton: Instancia única del logger
    """
    return LoggerSingleton()