from fastapi import FastAPI, HTTPException
from app.music import Music, CreateMusic


musics: list[Music] = [
    #Music(0, 'Experience', '16th april, 2020'),
    #Music(1, 'Fly(Moscow)', '8th april, 2012'),
    #Music(2, 'Una Mattina', '6th april, 2012'),
    #Music(3, 'My time', '21 January, 2012')
]

def add_musics(content: CreateMusic):
    id = len(musics)
    musics.append(Music(id, content.name, content.datasozd))
    return id

app = FastAPI()


########
# Jaeger

from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Service name is required for most backends,
# and although it's not necessary for console export,
# it's good to set service name anyways.
resource = Resource(attributes={
    SERVICE_NAME: "music-service"
})

jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831,
)

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(jaeger_exporter)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

FastAPIInstrumentor.instrument_app(app)

#
########

########
# Prometheus

from prometheus_fastapi_instrumentator import Instrumentator

@app.on_event("startup")
async def startup():
    Instrumentator().instrument(app).expose(app)

#
########

@app.get("/v1/musics")
async def get_musics():
    return musics

@app.post("/v1/musics")
async def add_music(content: CreateMusic):
    add_musics(content)
    return musics[-1]

@app.get("/v1/musics/{id}")
async def get_musics_by_id(id: int):
    result = [item for item in musics if item.id == id]
    if len(result) > 0:
        return result[0]
    raise HTTPException(status_code = 404, detail="Трек не найден")

@app.get("/__health")
async def check_service():
    return