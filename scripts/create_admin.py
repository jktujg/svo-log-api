import asyncio
import sys
from getpass import getpass
from contextlib import asynccontextmanager
from app.auth.permissions import UserRole, UserState
from app.dependencies import get_async_session
from app.auth.service import register_user
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-e', '--email', default=None)
parser.add_argument('-p', '--password', default=None)
args = parser.parse_args()

email = args.email or input('Email: ')
password = args.password or getpass(prompt='Password: ')
password_confirm = args.password or getpass(prompt='Password confirm: ')

if password != password_confirm:
    print('Password does not match')


async def register_admin(email, password):
    try:
        async with asynccontextmanager(get_async_session)() as session:
            user = await register_user(session=session, email=email, password=password, role=UserRole.ADMIN, state=UserState.ACTIVE)
    except Exception as err:
        print(err)
    else:
        print(f'Admin {email} successfully created')


if __name__ == '__main__':
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(register_admin(email, password))