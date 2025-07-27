import { Card, Col, Container, Row } from "react-bootstrap";

export function DashboardSkeleton() {
  return (
    <Container className="py-4">
      <div className="mb-4">
        <div className="skeleton" style={{ width: "200px", height: "2rem" }} />
      </div>
      
      <Row className="g-4 mb-4">
        {[1, 2, 3, 4].map((i) => (
          <Col key={i} md={6} lg={3}>
            <Card>
              <Card.Body>
                <div className="skeleton mb-2" style={{ width: "100px", height: "1rem" }} />
                <div className="skeleton" style={{ width: "150px", height: "2rem" }} />
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>

      <Row className="g-4">
        <Col lg={8}>
          <Card>
            <Card.Body>
              <div className="skeleton mb-3" style={{ width: "150px", height: "1.5rem" }} />
              <div className="skeleton" style={{ width: "100%", height: "200px" }} />
            </Card.Body>
          </Card>
        </Col>
        <Col lg={4}>
          <Card>
            <Card.Body>
              <div className="skeleton mb-3" style={{ width: "150px", height: "1.5rem" }} />
              {[1, 2, 3].map((i) => (
                <div key={i} className="mb-3">
                  <div className="skeleton" style={{ width: "100%", height: "3rem" }} />
                </div>
              ))}
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}

export function TableSkeleton({ rows = 5 }: { rows?: number }) {
  return (
    <div className="table-responsive">
      <table className="table">
        <thead>
          <tr>
            {[1, 2, 3, 4, 5].map((i) => (
              <th key={i}>
                <div className="skeleton" style={{ width: "100px", height: "1rem" }} />
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {Array.from({ length: rows }).map((_, i) => (
            <tr key={i}>
              {[1, 2, 3, 4, 5].map((j) => (
                <td key={j}>
                  <div className="skeleton" style={{ width: "80px", height: "1rem" }} />
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}