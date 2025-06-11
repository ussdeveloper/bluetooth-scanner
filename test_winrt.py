try:
    import winrt.windows.foundation.collections
    print('WinRT available')
except ImportError as e:
    print('WinRT not available:', e)
