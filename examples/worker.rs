pub fn fetch_all(urls: &[&str]) -> Vec<Conn> {
    let mut out = Vec::new();
    for url in urls {
        if let Ok(conn) = open(url) {
            out.push(conn);
        }
    }
    out
}

pub fn warm(url: &str) {
    let _ = open(url);
    let _ = open(url);
}
