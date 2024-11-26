from fastapi import FastAPI, APIRouter
import importlib
from pathlib import Path

# Initialize FastAPI app
app = FastAPI()

main_router = APIRouter()

# Dynamically import all feature routers
api_folder = Path(__file__).parent / 'api'

# Define the version prefix
version_prefix = "/v1"

# Iterate through all subfolders inside 'api' to dynamically register routes
for feature_folder in api_folder.iterdir():
    if feature_folder.is_dir():
        try:
            # Construct the module path for the feature's API
            module_name = f"api.{feature_folder.name}.api"
            feature_module = importlib.import_module(module_name)

            # Ensure the module has a router object
            if hasattr(feature_module, "router"):
                # Prepend '/v1' to all feature routes
                main_router.include_router(
                    feature_module.router,
                    prefix=f"{version_prefix}/{feature_folder.name}",
                    # Optional, useful for Swagger docs
                    tags=[feature_folder.name.capitalize()]
                )
                print(f"Successfully included routes for {
                      feature_folder.name}")
            else:
                print(f"No 'router' object found in {module_name}")
        except ImportError as e:
            print(f"Error importing module for {feature_folder.name}: {e}")
        except Exception as e:
            print(f"Unexpected error with {feature_folder.name}: {e}")

# Include the main router with versioning
app.include_router(main_router)
