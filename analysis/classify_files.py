import csv
import json
from pathlib import Path

INVENTORY_DIR = Path("raw_data/file_inventory")
OUTPUT_FILE = Path("analysis/public_internal_classification.csv")

# Classification based on FastAPI 0.162.4 documentation
# and its public package exports.
#
# Public: documented API or module directly supporting a documented API.
# Internal: implementation, compatibility, or supporting code without
# evidence of a documented public API.

PUBLIC = {
    "fastapi/__init__.py": (
        "Package entry point",
        "fastapi/__init__.py",
        "Re-exports documented FastAPI classes and functions."
    ),
    "fastapi/applications.py": (
        "Documented API",
        "reference/fastapi.md",
        "Defines the documented FastAPI application class."
    ),
    "fastapi/background.py": (
        "Documented API",
        "reference/background.md",
        "Defines the documented BackgroundTasks class."
    ),
    "fastapi/datastructures.py": (
        "Documented API",
        "reference/uploadfile.md",
        "Provides the documented UploadFile API."
    ),
    "fastapi/exceptions.py": (
        "Documented API",
        "reference/exceptions.md",
        "Defines documented HTTPException and WebSocketException."
    ),
    "fastapi/encoders.py": (
        "Documented API",
        "reference/encoders.md",
        "Defines the documented jsonable_encoder function."
    ),
    "fastapi/param_functions.py": (
        "Documented API",
        "reference/parameters.md",
        "Provides documented parameter declaration functions."
    ),
    "fastapi/params.py": (
        "Public API implementation",
        "reference/parameters.md",
        "Provides parameter classes underlying documented parameter declarations."
    ),
    "fastapi/requests.py": (
        "Documented API",
        "reference/request.md",
        "Defines documented Request and HTTPConnection interfaces."
    ),
    "fastapi/responses.py": (
        "Documented API",
        "reference/responses.md",
        "Defines documented response classes."
    ),
    "fastapi/routing.py": (
        "Documented API",
        "reference/apirouter.md",
        "Defines the documented APIRouter interface."
    ),
    "fastapi/security/__init__.py": (
        "Public API namespace",
        "reference/security/",
        "Provides the security API namespace used by documented security classes."
    ),
    "fastapi/security/api_key.py": (
        "Documented API",
        "reference/security/",
        "Defines documented API key security classes."
    ),
    "fastapi/security/http.py": (
        "Documented API",
        "reference/security/",
        "Defines documented HTTP authentication classes."
    ),
    "fastapi/security/oauth2.py": (
        "Documented API",
        "reference/security/",
        "Defines documented OAuth2 classes."
    ),
    "fastapi/security/open_id_connect_url.py": (
        "Documented API",
        "reference/security/",
        "Defines the documented OpenID Connect interface."
    ),
    "fastapi/sse.py": (
        "Documented API",
        "reference/sse.md",
        "Defines documented server-sent event classes."
    ),
    "fastapi/staticfiles.py": (
        "Documented API",
        "reference/staticfiles.md",
        "Defines the documented StaticFiles interface."
    ),
    "fastapi/templating.py": (
        "Documented API",
        "reference/templating.md",
        "Defines the documented Jinja2Templates interface."
    ),
    "fastapi/testclient.py": (
        "Documented API",
        "reference/testclient.md",
        "Defines the documented TestClient interface."
    ),
    "fastapi/websockets.py": (
        "Documented API",
        "reference/websockets.md",
        "Defines documented WebSocket interfaces."
    ),
    "fastapi/cli.py": (
        "Documented user-facing interface",
        "fastapi-cli.md",
        "Implements the FastAPI command-line interface documented by the project."
    ),
    "fastapi/middleware/__init__.py": (
        "Public API namespace",
        "advanced/middleware.md",
        "The documentation identifies fastapi.middleware as a developer-facing convenience namespace."
    ),
    "fastapi/middleware/cors.py": (
        "Documented API",
        "reference/middleware.md",
        "Provides the documented CORSMiddleware."
    ),
    "fastapi/middleware/gzip.py": (
        "Documented API",
        "reference/middleware.md",
        "Provides the documented GZipMiddleware."
    ),
    "fastapi/middleware/httpsredirect.py": (
        "Documented API",
        "reference/middleware.md",
        "Provides the documented HTTPSRedirectMiddleware."
    ),
    "fastapi/middleware/trustedhost.py": (
        "Documented API",
        "reference/middleware.md",
        "Provides the documented TrustedHostMiddleware."
    ),
    "fastapi/middleware/wsgi.py": (
        "Deprecated public interface",
        "advanced/wsgi.md",
        "Previously documented WSGIMiddleware interface; now deprecated in favour of a2wsgi."
    ),
    "fastapi/openapi/docs.py": (
        "Documented API",
        "reference/openapi/",
        "Defines documented OpenAPI documentation rendering functions."
    ),
    "fastapi/openapi/models.py": (
        "Documented API",
        "reference/openapi/",
        "Provides documented OpenAPI models."
    ),
}

INTERNAL_REASON = (
    "No direct public API documentation or package-level public export "
    "was identified in the 0.162.4 reference used for this classification."
)

INTERNAL = {
    "fastapi/__main__.py": "Command execution entry-point wrapper.",
    "fastapi/_compat.py": "Compatibility implementation.",
    "fastapi/_compat/__init__.py": "Compatibility package implementation.",
    "fastapi/_compat/main.py": "Compatibility implementation.",
    "fastapi/_compat/may_v1.py": "Pydantic compatibility implementation.",
    "fastapi/_compat/model_field.py": "Compatibility model-field implementation.",
    "fastapi/_compat/shared.py": "Shared compatibility helpers.",
    "fastapi/_compat/v1.py": "Pydantic v1 compatibility implementation.",
    "fastapi/_compat/v2.py": "Pydantic v2 compatibility implementation.",
    "fastapi/concurrency.py": "Internal concurrency helpers.",
    "fastapi/dependencies/__init__.py": "Dependency implementation package.",
    "fastapi/dependencies/models.py": "Internal dependency models.",
    "fastapi/dependencies/utils.py": "Internal dependency resolution functions.",
    "fastapi/exception_handlers.py": "Internal exception handling implementation.",
    "fastapi/logger.py": "Internal logging support.",
    "fastapi/middleware/asyncexitstack.py": "Internal middleware implementation.",
    "fastapi/openapi/__init__.py": "OpenAPI implementation package.",
    "fastapi/openapi/constants.py": "Internal OpenAPI constants.",
    "fastapi/openapi/utils.py": "Internal OpenAPI generation helpers.",
    "fastapi/security/base.py": "Internal security base implementation.",
    "fastapi/security/utils.py": "Internal security helper functions.",
    "fastapi/temp_pydantic_v1_params.py": "Temporary Pydantic compatibility implementation.",
    "fastapi/types.py": "Internal type definitions and annotations.",
    "fastapi/utils.py": "Internal framework utility functions.",
    "fastapi/telemetry/__init__.py": "Internal telemetry package.",
    "fastapi/telemetry/_api.py": "Internal telemetry implementation.",
    "fastapi/telemetry/_asgi.py": "Internal telemetry implementation.",
    "fastapi/telemetry/_runtime.py": "Internal telemetry runtime implementation.",
}


def load_all_paths():
    all_paths = set()

    for inventory_file in INVENTORY_DIR.glob("*.json"):
        data = json.loads(inventory_file.read_text(encoding="utf-8"))

        for component in data.get("components", []):
            if component.get("qualifier") == "FIL":
                all_paths.add(component["path"])

    return all_paths


def main():
    paths = load_all_paths()

    classified_paths = set(PUBLIC) | set(INTERNAL)
    missing = paths - classified_paths
    extra = classified_paths - paths

    if missing or extra:
        print("CLASSIFICATION VALIDATION FAILED")

        if missing:
            print("\nUnclassified inventory paths:")
            for path in sorted(missing):
                print("-", path)

        if extra:
            print("\nClassification paths absent from inventories:")
            for path in sorted(extra):
                print("-", path)

        raise SystemExit(1)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)

        writer.writerow([
            "file",
            "classification",
            "evidence_type",
            "documentation_reference",
            "rationale"
        ])

        for path in sorted(paths):
            if path in PUBLIC:
                evidence, reference, rationale = PUBLIC[path]
                classification = "Public"
            else:
                classification = "Internal"
                evidence = "No direct public API evidence identified"
                reference = "FastAPI 0.162.4 documentation review"
                rationale = INTERNAL.get(path, INTERNAL_REASON)

            writer.writerow([
                path,
                classification,
                evidence,
                reference,
                rationale
            ])

    print("Classification generated successfully.")
    print("Unique files:", len(paths))
    print("Public files:", len(PUBLIC))
    print("Internal files:", len(INTERNAL))
    print("Output:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
