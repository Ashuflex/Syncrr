from threading import Lock, Thread
from typing import Any
import logging
import os

class SingletonMeta(type):
    """
    This is a thread-safe implementation of Singleton.
    https://refactoring.guru/design-patterns/singleton/python/example#example-1
    """

    _instances = {}

    _lock: Lock = Lock()
    """
    We now have a lock object that will be used to synchronize threads during
    first access to the Singleton.
    """

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        # Now, imagine that the program has just been launched. Since there's no
        # Singleton instance yet, multiple threads can simultaneously pass the
        # previous conditional and reach this point almost at the same time. The
        # first of them will acquire lock and will proceed further, while the
        # rest will wait here.
        with cls._lock:
            # The first thread to acquire the lock, reaches this conditional,
            # goes inside and creates the Singleton instance. Once it leaves the
            # lock block, a thread that might have been waiting for the lock
            # release may then enter this section. But since the Singleton field
            # is already initialized, the thread won't create a new object.
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Singleton_Global_Variables(metaclass=SingletonMeta):
    dry_run: bool
    logging_level: Any #Typing Astralo-Interstellaire
    """
    We'll use this property to prove that our Singleton really works.
    """

    def __init__(self) -> None:
        pass

    def enable_dry_run(self) -> None:
        self.dry_run = True

    def disable_dry_run(self) -> None:
        self.dry_run = False

    def set_logging_level(self,
                        logging_level: Any) -> None:
        self.logging_level = logging_level

    def set_dry_run_state(self) -> None:
        value_env = os.environ.get('DRY_RUN')
        if not (env_dry_run := os.environ.get('DRY_RUN')):
            raise ValueError("Please setup an environment variable DRY_RUN.")
        if value_env.lower() == "true":
            self.enable_dry_run()
        elif value_env.lower() == "false":
            self.disable_dry_run()
        else:
            raise ValueError(f"Cannot understand DRY_RUN value {value_env}")

    def get_dry_run_state(self) -> bool:
        try:
            return self.dry_run
        except AttributeError as exc:
            raise AttributeError(f"Please use enable_dry_run or disable_dry_run beforehand, {repr(exc)}")

    def detailed_message(self) -> Any:  #Typing Astralo-Interstellaire
        if self.dry_run:
            try:
                return self.logging_level
            except AttributeError as exc:
                raise AttributeError(f"logging_level was not initialized, please use set_logging_level beforehand, {repr(exc)}")
        else:
            return logging.DEBUG


    def counter_messages(self) -> Any:  #Typing Astralo-Interstellaire
        return self.logging_level
