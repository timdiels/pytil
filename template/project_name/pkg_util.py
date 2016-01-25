from project_name import __root__

def get_data_file(path):
    '''
    Get data path to file
    
    Parameters
    ----------
    path : str
        path to data file relative to data dir
    
    Returns
    -------
    plumbum.Path
        Path to data file
    '''
    return __root__ / 'data' / path
