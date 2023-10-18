from ellar.common import Module, exception_handler, IExecutionContext, JSONResponse, Response, IApplicationStartup
from ellar.core import App, ModuleBase
from ellar.samples.modules import HomeModule

from .todoapp.module import TodoappModule
from .users.module import UsersModule
from .db.database import get_engine
from .db.models import Base


@Module(modules=[HomeModule, TodoappModule, UsersModule])
class ApplicationModule(ModuleBase, IApplicationStartup):
    async def on_startup(self, app: App) -> None:
        Base.metadata.create_all(bind=get_engine(app.config))

    @exception_handler(404)
    def exception_404_handler(cls, ctx: IExecutionContext, exc: Exception) -> Response:
        return JSONResponse(dict(detail="Resource not found."))
