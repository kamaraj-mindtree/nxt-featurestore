import json
import threading
from typing import Callable, Optional

import pkg_resources
import uvicorn
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List
import feast

def get_app(
    store: "feast.FeatureStore",
    get_registry_dump: Callable,
    project_id: str,
    registry_ttl_secs: int,
    host: str,
    port: int,
):
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Asynchronously refresh registry, notifying shutdown and canceling the active timer if the app is shutting down
    registry_json = ""
    shutting_down = False
    active_timer: Optional[threading.Timer] = None

    def async_refresh():
        store.refresh_registry()
        nonlocal registry_json
        registry_json = get_registry_dump(store.config, store.repo_path)
        if shutting_down:
            return
        nonlocal active_timer
        active_timer = threading.Timer(registry_ttl_secs, async_refresh)
        active_timer.start()

    @app.on_event("shutdown")
    def shutdown_event():
        nonlocal shutting_down
        shutting_down = True
        if active_timer:
            active_timer.cancel()

    async_refresh()

    ui_dir = pkg_resources.resource_filename(__name__, "ui/build/")
    # Initialize with the projects-list.json file
    with open(ui_dir + "projects-list.json", mode="w") as f:
        projects_dict = {
            "projects": [
                {
                    "name": "Project",
                    "description": "Test project",
                    "id": project_id,
                    "registryPath": "/registry",
                }
            ]
        }
        f.write(json.dumps(projects_dict))

    @app.get("/registry")
    def read_registry():
        return json.loads(registry_json)

    @app.get("/nxt/feature-store-apply")
    def nxt_apply(parquet_path:str,entity_column:str,feature_views_name:str,feature_service_name:str):
        # print(path, entity_name, feature_view_name)
        from feast.nxt import nxt_fs_api
        # nxt_feature_store.feast_function(path, entity_name, feature_view_name)
        return nxt_fs_api.feast_function(parquet_path,entity_column,feature_views_name,feature_service_name)
    
    @app.post('/nxt/feature-retrieval')
    def nxt_feature_retrieval(entity_keys:str,entity_name: str,feature_view_names: str,start_date:str,end_date:str):
        from feast.nxt import nxt_fs_api
        return nxt_fs_api.register_entity_df(map(int,entity_keys.split(',')),entity_name,[feature_view_names],start_date.split('T')[0],end_date.split('T')[0])
    
    @app.post('/nxt/feature-materialize')
    def nxt_feature_materialize(start_date: str, end_date: str):
        from feast.nxt import nxt_fs_api
        return nxt_fs_api.materialize(start_date.split('T')[0],end_date.split('T')[0])
    

    # For all other paths (such as paths that would otherwise be handled by react router), pass to React
    @app.api_route("/p/{path_name:path}", methods=["GET"])
    def catch_all():
        filename = ui_dir + "index.html"

        with open(filename) as f:
            content = f.read()

        return Response(content, media_type="text/html")

    app.mount(
        "/", StaticFiles(directory=ui_dir, html=True), name="site",
    )

    return app


def start_server(
    store: "feast.FeatureStore",
    host: str,
    port: int,
    get_registry_dump: Callable,
    project_id: str,
    registry_ttl_sec: int,
):
    app = get_app(store, get_registry_dump, project_id, registry_ttl_sec, host, port)
    uvicorn.run(app, host=host, port=port)
