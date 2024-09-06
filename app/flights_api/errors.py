from fastapi import HTTPException, status


NOT_FOUND = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')