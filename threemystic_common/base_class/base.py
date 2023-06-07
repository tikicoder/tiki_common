import abc
from logging import Logger

class base(abc.ABC): 
  """This is a set of library wrappers to help general python apps"""

  def __init__(self, *args, **kwargs) -> None:
    super().__init__()
    self._custom_init_pre()

  def _custom_init_pre(self, *args, **kwargs):
    pass    
   
  
  def __init_main(self, main_reference, *args, **kwargs):
    if main_reference is not None:
      self._main_reference = main_reference
  
  def get_main(self, *args, **kwargs):
    if not hasattr(self, "_main_reference"):
      return self._main_reference
    
    return None

  def __logger_init(self, logger_name, logger = None, init_object = None,  refresh = False, *args, **kwargs):
    if hasattr(self, "_logger") and not refresh:
      if self._logger is not None:
        return

    if logger is not None or init_object is not None:
      self._logger = self.get_common().helper_type().logging().get_child_logger(
        child_logger_name= logger_name,
        logger= logger if init_object is None else init_object.get_logger()
      )

  def get_logger(self) -> Logger:
    if hasattr(self, "_logger"):
      return self._logger
    
    if hasattr(self, "_logger_name"):
      self._logger = self.get_main().get_logger().getChild(self._logger_name)
      return self.get_logger()
    
    return None
    

  def _unset(self, attribute, *args, **kwargs):
      if not hasattr(self, attribute):
        return

      delattr(self, attribute)
  
  def __init_common(self, init_object = None, common = None, refresh = False, force_skip_getcommon = False, *args, **kwargs):
    if hasattr(self, "_common") and not refresh:
      if self._common is not None:
        return self.get_common()

    if init_object is not None and hasattr(init_object, "get_common") and not force_skip_getcommon:
      self._common = init_object.get_common()
      return self.get_common()
    
    if common is None:
      from threemystic_common.common import common as threemystic_common
      self._common = threemystic_common()
      self.get_common()
  
  def get_common(self, *args, **kwargs):
    if hasattr(self, "_common"):
      if self._common is not None:
        return self._common
    
    self.__init_common(force_skip_getcommon= True)
    return self.get_common()
      