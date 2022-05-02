pub mod routeguide {
    tonic::include_proto!("routeguide");
}

use async_stream::stream;
use rand::prelude::ThreadRng;
use rand::Rng;
use routeguide::route_guide_client::RouteGuideClient;
use routeguide::Point;
use std::error::Error;
use tonic::transport::Channel;
use tonic::Request;

fn random_point(rng: &mut ThreadRng) -> Point {
    let latitude = (rng.gen_range(0, 180) - 90) * 10_000_000;
    let longitude = (rng.gen_range(0, 360) - 180) * 10_000_000;
    Point {
        latitude,
        longitude,
    }
}

async fn run_record_route(client: &mut RouteGuideClient<Channel>) -> Result<(), Box<dyn Error>> {
    let mut rng = rand::thread_rng();
    let point_count: usize = 5;

    let mut points = vec![];
    for _ in 0..point_count {
        points.push(random_point(&mut rng))
    }
    let early_return_index = rng.gen_range(0_usize, point_count - 1);
    points[early_return_index].latitude = 0;
    println!("early_return_index = {}", early_return_index);

    let s = stream! {
        for point in points {
            yield point;
            println!("Sleep for 500 ms");
            tokio::time::sleep(std::time::Duration::from_millis(500)).await;
        }
    };

    let request = Request::new(s);

    match client.record_route(request).await {
        Ok(response) => println!("SUMMARY: {:?}", response.into_inner()),
        Err(e) => println!("something went wrong: {:?}", e),
    }

    Ok(())
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let port = std::env::args()
        .nth(1)
        .unwrap_or_else(|| "5000".to_string());
    println!("port = {}", port);
    let mut client = RouteGuideClient::connect(format!("http://[::]:{}", port)).await?;
    run_record_route(&mut client).await?;
    Ok(())
}
