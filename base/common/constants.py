from base.common.names import *

# using this instead of . is necessary to find the current working directory's path on android
here = os.path.abspath(".") + "/"

IS_WEB = __import__("sys").platform == "emscripten"
IS_ANDROID = "ANDROID_ARGUMENT" in os.environ
IS_DESKTOP = False # TBF