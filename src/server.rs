#[derive(Debug)]
struct RouteGuideService;

pub mod routeguide {
    tonic::include_proto!("routeguide");
}

use routeguide::route_guide_server::{RouteGuide, RouteGuideServer};
use routeguide::{Point, RouteSummary};
use tokio_stream::StreamExt;
use tonic::transport::Server;
use tonic::{Request, Response, Status, Streaming};

#[tonic::async_trait]
impl RouteGuide for RouteGuideService {
    async fn record_route(
        &self,
        request: Request<Streaming<Point>>,
    ) -> Result<Response<RouteSummary>, Status> {
        let mut stream = request.into_inner();

        let mut summary = RouteSummary::default();

        while let Some(point) = stream.next().await {
            let point = point?;
            summary.point_count += 1;

            if point.latitude == 0 {
                println!("Return early: {}", summary.point_count);
                return Ok(Response::new(summary));
            }
        }
        println!("Return normal: {}", summary.point_count);
        Ok(Response::new(summary))
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let addr = "[::]:5000".parse().unwrap();

    let route_guide = RouteGuideService {};

    let svc = RouteGuideServer::new(route_guide);

    Server::builder().add_service(svc).serve(addr).await?;

    Ok(())
}
