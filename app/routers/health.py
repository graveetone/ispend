from fastapi import APIRouter, status

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def health():
    return {"status": "Money loves me"}


@router.get("/version", status_code=status.HTTP_200_OK)
async def app_version():
    from version import VERSION, COMMIT
    return {"version": VERSION, "commit": COMMIT}
