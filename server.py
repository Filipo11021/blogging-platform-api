import uvicorn
import os

if __name__ == '__main__':
    uvicorn.run(
        'main:app', 
        host=os.getenv('HOST', 'localhost'), 
        port=os.getenv('PORT', 4000), 
        log_level='info' )
