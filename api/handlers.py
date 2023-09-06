from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello World"}

# create_database - <DB_name> <structure>
# get -     <DB_name> <field_name> <value>
# create -  <DB_name> <obj structure>
# delete -  <DB_name> <field_name> <value>
# update -  <DB_name> <field_name> <value> <field_for_update> <value_for_update>
